# =====================================================================
#  MODELO 1 - ANCHO DEL CORDON
#  Jerarquico bayesiano con efecto aleatorio por estudio
#
#  Pregunta que responde:
#     ¿cuanto de la variacion del ancho la explica el LABORATORIO
#      y cuanto la explican los PARAMETROS?
#
#  Requisitos:  install.packages(c("brms","dplyr","readr","ggplot2"))
#               brms necesita Stan; la primera vez tarda en compilar.
# =====================================================================

library(readr); library(dplyr); library(brms); library(ggplot2)

# En Mac ARM el motor rstan falla por un conflicto de TBB.
# cmdstanr es el backend recomendado y evita el problema.
suppressMessages(library(cmdstanr))
options(brms.backend = "cmdstanr", mc.cores = 4)

# ---------------------------------------------------------------- DATOS
d <- read_csv("MODELADO.csv", show_col_types = FALSE) |>
  filter(!is.na(W_mm), !is.na(WFS_TS), !is.na(TS_mm_s)) |>
  mutate(
    estudio   = factor(paper_id),
                            # cladding | BOP
    familia   = factor(if_else(grepl("316|317|308|2209|2507|2594|inox",
                                     alambre_clase), "inox", "carbono")),
    # logaritmos: las relaciones del proceso son multiplicativas.
    # Ademas, un error de ESCALA en un estudio (p.ej. unidades mal rotuladas)
    # se convierte en un corrimiento constante que el efecto aleatorio absorbe.
    lW        = log(W_mm),
    lQ        = log(WFS_TS)  - mean(log(WFS_TS)),          # centrado
    lTS       = log(TS_mm_s) - mean(log(TS_mm_s))
  )

cat("n =", nrow(d), " estudios =", nlevels(d$estudio), "\n")
print(table(d$familia))

# ------------------------------------------------------- PISO DE ERROR
# Medido en las replicas verdaderas del propio corpus (hoja 11_PISO_ERROR).
# El ancho tiene CV = 3.84 %  ->  en escala log, 0.0384.
#
# CORRECCION (2026-09-14, H-082): el piso es la variacion entre replicas con
# parametros IDENTICOS. El residuo del modelo incluye ademas toda la variacion
# intra-estudio que lQ, lTS, aplic y familia NO explican (voltaje, CTWD, gas...),
# y resulta ~0.11, tres veces el piso. Anclar el prior de sigma al piso
# (normal(0.0384, 0.02)) daba probabilidad 6e-5 al valor observado: mal
# especificado. Los datos lo vencieron (218 obs), pero se corrige a un prior
# debilmente informativo. El piso se usa DESPUES, como cota inferior contra la
# que se juzga el residuo, no como su valor esperado.
CV_ANCHO <- 0.0384

pr <- c(
  prior(normal(2.5, 1),        class = "Intercept"),   # log(12.8 mm) ~ 2.55
  prior(normal(0, 0.5),        class = "b"),           # efectos moderados
  prior(exponential(1),        class = "sd"),          # sd entre estudios
  prior(student_t(3, 0, 0.25), class = "sigma", lb = 0) # debilmente informativo
)

# ------------------------------------------------------------- MODELO
# (1 | estudio) = intercepto aleatorio: el desvio propio de cada laboratorio.
# ESE termino es el equivalente estadistico del factor de calibracion
# que despues estimaras en tu taller con las probetas.
m1 <- brm(
  lW ~ lQ + lTS + familia + (1 | estudio),
  data = d, family = gaussian(), prior = pr,
  chains = 4, iter = 4000, warmup = 1000, cores = 4, seed = 1, refresh = 0,
  control = list(adapt_delta = 0.95)
)

print(summary(m1))

# ------------------------------------------- ¿CUANTO PESA EL LABORATORIO?
vc        <- VarCorr(m1)
sd_lab    <- vc$estudio$sd[1, "Estimate"]
sd_resid  <- as.numeric(summary(m1)$spec_pars["sigma", "Estimate"])
icc       <- sd_lab^2 / (sd_lab^2 + sd_resid^2)

cat("\n=========================================================\n")
cat(" RESULTADO PRINCIPAL\n")
cat("=========================================================\n")
cat(sprintf("  sd entre laboratorios : %.4f  (log)  ~ %.1f %%\n", sd_lab,   100*(exp(sd_lab)-1)))
cat(sprintf("  sd residual (ruido)   : %.4f  (log)  ~ %.1f %%\n", sd_resid, 100*(exp(sd_resid)-1)))
cat(sprintf("  ICC = %.3f  ->  el laboratorio explica el %.0f %% de la varianza\n", icc, 100*icc))
cat("\n  Piso de error medido en replicas: 3.84 %\n")
cat("  Si sd_resid se aproxima a ese valor, el modelo ya toco el techo\n")
cat("  de precision del proceso: no hay mas senal que capturar.\n")

# --------------------------------------- DESVIO DE CADA LABORATORIO
# Esto es lo que tus probetas estimaran para TU taller.
re <- ranef(m1)$estudio[, , "Intercept"] |> as.data.frame() |>
      tibble::rownames_to_column("estudio") |>
      mutate(desvio_pct = 100*(exp(Estimate) - 1)) |>
      arrange(desvio_pct)
cat("\n  Desvio de cada laboratorio respecto al promedio:\n")
print(re[, c("estudio","Estimate","desvio_pct")], row.names = FALSE)

# ------------------------------------ VALIDACION DEJANDO-UN-LAB-FUERA
cat("\n  Validacion dejando-un-laboratorio-fuera...\n")
res <- lapply(levels(d$estudio), function(L) {
  tr <- filter(d, estudio != L); te <- filter(d, estudio == L)
  fit <- update(m1, newdata = tr, refresh = 0)
  # re_formula = NA -> predice SIN conocer el desvio del laboratorio nuevo,
  # que es exactamente la situacion de tu taller antes de calibrar.
  p  <- colMeans(posterior_epred(fit, newdata = te, allow_new_levels = TRUE,
                                 re_formula = NA))
  data.frame(estudio = L, n = nrow(te),
             MAPE = mean(abs(exp(p) - te$W_mm) / te$W_mm) * 100)
}) |> bind_rows()

print(res, row.names = FALSE)
cat(sprintf("\n  MAPE medio sin calibrar = %.1f %%   (piso experimental: 3.8 %%)\n",
            mean(res$MAPE)))
cat("  La diferencia entre ambos es LO QUE LA CALIBRACION PUEDE RECUPERAR.\n")

saveRDS(m1, "modelo_01_ancho.rds")
write_csv(res, "validacion_lolo_ancho_A.csv")
cat("\n  Guardados: modelo_01_ancho.rds y validacion_lolo_ancho_A.csv\n")
