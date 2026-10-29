# =====================================================================
#  MODELO 3 (bayesiano) - TODAS LAS RESPUESTAS + MODELO CONJUNTO
#
#  Parte 1  Especificacion G (sin imputados + tecnica) para W, R, P, D, IC, W/P.
#           ICC ajustado, R2 marginal/condicional (Nakagawa 2017) con IC 95 %.
#
#  Parte 2  MODELO MULTIVARIANTE  W + R + P  con interceptos aleatorios
#           CORRELACIONADOS por estudio:  (1 | p | estudio)
#           Aprovecha toda la informacion de cada laboratorio a la vez y
#           responde una pregunta nueva: ¿un laboratorio que "ve" cordones
#           mas anchos tambien los ve mas penetrados? La matriz de
#           correlacion de los desvios de laboratorio es el resultado.
#
#  Se ejecuta desde dataset/. Requiere MODELADO.csv con WFS_origen y tecnica.
# =====================================================================
suppressMessages({library(readr); library(dplyr); library(brms); library(cmdstanr); library(tidyr)})
options(brms.backend = "cmdstanr", mc.cores = 4)
IMPUTADOS <- c("03_Palani2006", "04_Palani2007", "07_Kumar2011")
PISO <- c(W_mm=.0384, R_mm=.0287, P_mm=.0792, D_pct=.1020, IC_pct=.0609, W_P=.0896)

d0 <- read_csv("MODELADO.csv", show_col_types = FALSE) |>
  filter(!paper_id %in% IMPUTADOS, !is.na(WFS_TS), !is.na(TS_mm_s)) |>
  mutate(estudio = factor(paper_id),  tecnica = factor(tecnica),
         familia = factor(if_else(grepl("316|317|308|2209|2507|2594|inox", alambre_clase), "inox", "carbono")),
         lQ = log(WFS_TS) - mean(log(WFS_TS)), lTS = log(TS_mm_s) - mean(log(TS_mm_s)))

pr <- c(prior(normal(0, 0.5), class = "b"), prior(exponential(1), class = "sd"),
        prior(student_t(3, 0, 0.25), class = "sigma", lb = 0))

# factores no redundantes (evita matriz singular, p.ej. dilucion: aplic == familia)
terminos <- function(d) {
  f <- c(); part <- list()
  for (v in c("familia", "tecnica")) {
    if (nlevels(droplevels(d[[v]])) < 2) next
    p <- as.integer(droplevels(d[[v]]))
    if (any(vapply(part, function(q) identical(q, p), logical(1)))) next
    part[[length(part) + 1]] <- p; f <- c(f, v)
  }
  paste(c("lQ", "lTS", f), collapse = " + ")
}
q <- function(x) sprintf("%.3f [%.3f, %.3f]", median(x), quantile(x, .025), quantile(x, .975))

# ------------------------------------------------------------ PARTE 1
cat("\n=========== PARTE 1 - especificacion G por respuesta (bayesiano) ===========\n")
res <- lapply(names(PISO), function(y) {
  d <- d0 |> filter(!is.na(.data[[y]])) |> mutate(ly = log(.data[[y]]))
  f <- as.formula(paste("ly ~", terminos(d), "+ (1 | estudio)"))
  m <- brm(f, data = d, family = gaussian(), prior = pr, chains = 4, iter = 4000, warmup = 1000,
           seed = 1, refresh = 0, control = list(adapt_delta = 0.99))
  dr <- as_draws_df(m); sdl <- dr$sd_estudio__Intercept; sg <- dr$sigma
  tibble(respuesta = y, n = nrow(d), estudios = nlevels(droplevels(d$estudio)),
         b_lQ = q(dr$b_lQ), b_lTS = q(dr$b_lTS),
         ICC_aj = q(sdl^2/(sdl^2+sg^2)),
         R2_marg = q(bayes_R2(m, re_formula = NA, summary = FALSE)[,1]),
         R2_cond = q(bayes_R2(m, summary = FALSE)[,1]),
         sigma = q(sg), sigma_piso = sprintf("%.2f", median(sg)/PISO[[y]]),
         diverg = sum(nuts_params(m, pars = "divergent__")$Value))
}) |> bind_rows()
print(as.data.frame(res), row.names = FALSE, right = FALSE)
write_csv(res, "malla_todas_respuestas_bayes.csv")

# ------------------------------------------------------------ PARTE 2
cat("\n=========== PARTE 2 - modelo CONJUNTO W + R + P, desvios de laboratorio correlacionados ===========\n")
dm <- d0 |> filter(!is.na(W_mm), !is.na(R_mm), !is.na(P_mm)) |>
  mutate(lW = log(W_mm), lR = log(R_mm), lP = log(P_mm))
cat("n =", nrow(dm), " estudios =", nlevels(droplevels(dm$estudio)), "\n")
tm <- terminos(dm)
fm <- bf(as.formula(paste("lW ~", tm, "+ (1 | p | estudio)"))) +
      bf(as.formula(paste("lR ~", tm, "+ (1 | p | estudio)"))) +
      bf(as.formula(paste("lP ~", tm, "+ (1 | p | estudio)"))) + set_rescor(TRUE)
# en modelos multivariantes cada prior debe llevar resp=
prm <- prior(lkj(2), class = "cor")
for (r in c("lW", "lR", "lP")) prm <- prm +
  set_prior("normal(0, 0.5)",         class = "b",     resp = r) +
  set_prior("exponential(1)",         class = "sd",    resp = r) +
  set_prior("student_t(3, 0, 0.25)",  class = "sigma", resp = r, lb = 0)
mm <- brm(fm, data = dm, prior = prm, chains = 4, iter = 4000, warmup = 1000, seed = 1, refresh = 0,
          control = list(adapt_delta = 0.99))
dr <- as_draws_df(mm)
cat("\nCorrelacion de los DESVIOS DE LABORATORIO entre respuestas (mediana [IC 95 %]):\n")
cat("  W ~ R :", q(dr$cor_estudio__lW_Intercept__lR_Intercept), "\n")
cat("  W ~ P :", q(dr$cor_estudio__lW_Intercept__lP_Intercept), "\n")
cat("  R ~ P :", q(dr$cor_estudio__lR_Intercept__lP_Intercept), "\n")
cat("\nCorrelacion RESIDUAL entre respuestas (dentro de estudio):\n")
cat("  W ~ R :", q(dr$rescor__lW__lR), "\n")
cat("  W ~ P :", q(dr$rescor__lW__lP), "\n")
cat("  R ~ P :", q(dr$rescor__lR__lP), "\n")
cat("\nICC ajustado por respuesta en el modelo conjunto:\n")
for (y in c("lW", "lR", "lP")) {
  sdl <- dr[[paste0("sd_estudio__", y, "_Intercept")]]; sg <- dr[[paste0("sigma_", y)]]
  cat(sprintf("  %s : %s\n", y, q(sdl^2/(sdl^2+sg^2))))
}
cat("\nb_lQ conjunto:  W", q(dr$b_lW_lQ), " R", q(dr$b_lR_lQ), " P", q(dr$b_lP_lQ), "\n")
cat("divergentes:", sum(nuts_params(mm, pars = "divergent__")$Value), "\n")
saveRDS(mm, "modelo_conjunto_WRP.rds")
cat("\nGuardados: malla_todas_respuestas_bayes.csv · modelo_conjunto_WRP.rds\n")
