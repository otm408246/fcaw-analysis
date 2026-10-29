# =====================================================================
#  MODELO 2 - SENSIBILIDAD DEL ANCHO, version bayesiana (brms + cmdstanr)
#
#  Ajusta las tres configuraciones que se reportan en la tesis y calcula
#  las cantidades de Nakagawa et al. (2017) desde el posterior:
#     ICC ajustado = sd_estudio^2 / (sd_estudio^2 + sigma^2)
#     R2 marginal  = bayes_R2 sin efectos aleatorios (solo parametros)
#     R2 condicional = bayes_R2 con efectos aleatorios (parametros + lab)
#
#  A  todo                          218 corridas · 10 estudios
#  B  sin los 3 imputados (H-048)   160 · 7
#  G  sin imputados + tecnica       160 · 7   <- especificacion preferida
#
#  Requiere MODELADO.csv con WFS_origen y tecnica
#  (_scripts/wfs_origen_y_tecnica.py). Se ejecuta desde dataset/.
# =====================================================================
suppressMessages({library(readr); library(dplyr); library(brms); library(cmdstanr)})
options(brms.backend = "cmdstanr", mc.cores = 4)

IMPUTADOS <- c("03_Palani2006", "04_Palani2007", "07_Kumar2011")

d0 <- read_csv("MODELADO.csv", show_col_types = FALSE) |>
  filter(!is.na(W_mm), !is.na(WFS_TS), !is.na(TS_mm_s)) |>
  mutate(estudio = factor(paper_id),  tecnica = factor(tecnica),
         familia = factor(if_else(grepl("316|317|308|2209|2507|2594|inox", alambre_clase), "inox", "carbono")),
         lW = log(W_mm))

pr <- c(prior(normal(2.5, 1),        class = "Intercept"),
        prior(normal(0, 0.5),        class = "b"),
        prior(exponential(1),        class = "sd"),
        prior(student_t(3, 0, 0.25), class = "sigma", lb = 0))   # corregido, H-082

ajustar <- function(d, con_tecnica = FALSE, nombre) {
  d <- d |> mutate(lQ = log(WFS_TS) - mean(log(WFS_TS)), lTS = log(TS_mm_s) - mean(log(TS_mm_s)))
  f <- if (con_tecnica) lW ~ lQ + lTS + familia + tecnica + (1 | estudio)
       else              lW ~ lQ + lTS + familia + (1 | estudio)
  m <- brm(f, data = d, family = gaussian(), prior = pr,
           chains = 4, iter = 4000, warmup = 1000, seed = 1, refresh = 0,
           control = list(adapt_delta = 0.95))
  dr  <- as_draws_df(m)
  sdl <- dr$sd_estudio__Intercept; sg <- dr$sigma
  icc <- sdl^2 / (sdl^2 + sg^2)
  r2m <- bayes_R2(m, re_formula = NA, summary = FALSE)[, 1]
  r2c <- bayes_R2(m, summary = FALSE)[, 1]
  q <- function(x) sprintf("%.3f [%.3f, %.3f]", median(x), quantile(x, .025), quantile(x, .975))
  tibble(config = nombre, n = nrow(d), estudios = nlevels(droplevels(d$estudio)),
         ICC_aj = q(icc), R2_marg = q(r2m), R2_cond = q(r2c),
         sd_lab = q(sdl), sigma = q(sg),
         b_lQ = q(dr$b_lQ), b_lTS = q(dr$b_lTS),
         divergentes = sum(nuts_params(m, pars = "divergent__")$Value))
}

res <- bind_rows(
  ajustar(d0,                                    FALSE, "A  todo"),
  ajustar(filter(d0, !paper_id %in% IMPUTADOS),  FALSE, "B  sin imputados"),
  ajustar(filter(d0, !paper_id %in% IMPUTADOS),  TRUE,  "G  sin imputados + tecnica"))

cat("\n=================================================================================\n")
cat(" SENSIBILIDAD BAYESIANA DEL ANCHO - mediana [IC 95 %]   (Nakagawa et al. 2017)\n")
cat("=================================================================================\n")
print(as.data.frame(res), row.names = FALSE, right = FALSE)
cat("\n  piso de error del ancho (H-034): 0.0384 en log. sigma debe quedar POR ENCIMA.\n")
write_csv(res, "sensibilidad_ancho_bayes.csv")
cat("  Guardado: sensibilidad_ancho_bayes.csv\n")
