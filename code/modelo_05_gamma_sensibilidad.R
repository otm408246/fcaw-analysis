# modelo_05 · ejecutado el 2026-10-13. Salida: malla_gamma_vs_log.csv
# Sensibilidad (McCullagh y Nelder, 1989, cap. 8): normal sobre log(y) frente a GLM gamma con enlace log.
# Misma especificación G y mismos priors que modelo_03_todas_respuestas.R. No escribe en la carpeta del proyecto.
suppressPackageStartupMessages({library(brms); library(readr); library(dplyr)})
options(brms.backend = "cmdstanr", mc.cores = 4)
# run from data/: cd data && Rscript ../code/modelo_05_gamma_sensibilidad.R
IMPUTADOS <- c("03_Palani2006", "04_Palani2007", "07_Kumar2011")
d0 <- read_csv("MODELADO.csv", show_col_types = FALSE) |>
  filter(!paper_id %in% IMPUTADOS, !is.na(WFS_TS), !is.na(TS_mm_s)) |>
  mutate(estudio = factor(paper_id), tecnica = factor(tecnica),
         familia = factor(if_else(grepl("316|317|308|2209|2507|2594|inox", alambre_clase), "inox", "carbono")),
         lQ = log(WFS_TS) - mean(log(WFS_TS)), lTS = log(TS_mm_s) - mean(log(TS_mm_s)))
factores <- function(d, cands) {           # igual que modelo_03: >1 nivel y sin repetir partición
  out <- c(); vistas <- list()
  for (v in cands) { p <- as.integer(factor(d[[v]]))
    if (length(unique(p)) < 2) next
    if (any(sapply(vistas, function(q) identical(q, p)))) next
    vistas[[length(vistas)+1]] <- p; out <- c(out, v) }
  out }
pr_n <- c(prior(normal(0, 0.5), class = "b"), prior(exponential(1), class = "sd"),
          prior(student_t(3, 0, 0.25), class = "sigma", lb = 0))
pr_g <- c(prior(normal(0, 0.5), class = "b"), prior(exponential(1), class = "sd"))
res <- list()
for (y in c("W_mm", "R_mm", "P_mm")) {
  d <- d0 |> filter(!is.na(.data[[y]])) |> mutate(yy = .data[[y]], ly = log(.data[[y]]))
  rhs <- paste(c("lQ", "lTS", factores(d, c("familia", "tecnica")), "(1 | estudio)"), collapse = " + ")
  mn <- brm(as.formula(paste("ly ~", rhs)), data = d, family = gaussian(), prior = pr_n,
            chains = 4, iter = 2000, seed = 1, refresh = 0, silent = 2, control = list(adapt_delta = 0.95))
  mg <- brm(as.formula(paste("yy ~", rhs)), data = d, family = Gamma(link = "log"), prior = pr_g,
            chains = 4, iter = 2000, seed = 1, refresh = 0, silent = 2, control = list(adapt_delta = 0.95))
  fn <- fixef(mn); fg <- fixef(mg)
  sn <- posterior_summary(mn, variable = c("sd_estudio__Intercept", "sigma"))
  sg <- posterior_summary(mg, variable = c("sd_estudio__Intercept", "shape"))
  cv_g <- 1 / sqrt(as_draws_df(mg)$shape)                         # CV del gamma = 1/sqrt(forma)
  div <- function(m) sum(nuts_params(m)$Value[nuts_params(m)$Parameter == "divergent__"])
  f <- function(x) sprintf("%.3f [%.3f, %.3f]", x[1], x[3], x[4])
  res[[y]] <- data.frame(respuesta = y, n = nrow(d), estudios = nlevels(droplevels(d$estudio)),
    b_lQ_normal_log = f(fn["lQ", ]), b_lQ_gamma = f(fg["lQ", ]),
    b_lTS_normal_log = f(fn["lTS", ]), b_lTS_gamma = f(fg["lTS", ]),
    sd_estudio_normal_log = f(sn["sd_estudio__Intercept", ]), sd_estudio_gamma = f(sg["sd_estudio__Intercept", ]),
    resid_sigma_normal_log = f(sn["sigma", ]), resid_CV_gamma = sprintf("%.3f [%.3f, %.3f]", median(cv_g), quantile(cv_g,.025), quantile(cv_g,.975)),
    dif_intercepto = sprintf("%.4f", fg["Intercept","Estimate"] - fn["Intercept","Estimate"]),
    sigma2_medios = sprintf("%.4f", sn["sigma","Estimate"]^2 / 2),
    divergencias = paste(div(mn), div(mg), sep = " / "))
  cat("listo:", y, "\n")
}
out <- do.call(rbind, res); print(t(out))
write.csv(out, "malla_gamma_vs_log.csv", row.names = FALSE)
