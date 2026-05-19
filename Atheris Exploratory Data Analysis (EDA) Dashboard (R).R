library(tidyverse)
library(ggplot2)

# 1. Create the data frame
raw_data <- tibble(
  Condition = c("Factory New", "Minimal Wear", "Field-Tested", "Well-Worn", "Battle-Scarred"),
  `2019` = c(1033.2, 521.17, 293.2, 239.51, 200.39),
  `2020` = c(778.46, 378.46, 226.31, 182.13, 152.97),
  `2021` = c(750.84, 340.58, 189.41, 159.32, 138.37),
  `2022` = c(757.54, 350.59, 175.48, 132.45, 124.01),
  `2023` = c(846.13, 370.3, 203.43, 154.14, 137.6),
  `2024` = c(1015.79, 446.96, 235.0, 169.51, 153.33),
  `2025` = c(1120.55, 498.06, 284.79, 238.39, 228.26),
  `2026` = c(4339.02, 697.55, 414.11, 360.52, 332.67)
)

# 2. Tidy the data
cleaned_data <- raw_data %>%
  pivot_longer(
    cols = starts_with("20"), 
    names_to = "Year", 
    values_to = "Price_PHP"
  ) %>%
  mutate(
    Year = as.numeric(Year),
    Condition = factor(Condition, levels = c("Factory New", "Minimal Wear", "Field-Tested", "Well-Worn", "Battle-Scarred"))
  )

# 3. Plot the data (Publication-grade ggplot2)
ggplot(cleaned_data, aes(x = Year, y = Price_PHP, color = Condition, group = Condition)) +
  geom_line(linewidth = 1.2, alpha = 0.8) +
  geom_point(size = 3) +
  scale_y_continuous(labels = scales::dollar_format(prefix = "₱")) +
  scale_x_continuous(breaks = 2019:2026) +
  scale_color_viridis_d(option = "plasma", end = 0.85) + 
  labs(
    title = "AWP | Atheris Market Value (2019 - 2026)",
    subtitle = "Historical pricing data tracked via Steam Market in Philippine Peso (PHP)",
    x = "Year",
    y = "Price (PHP)",
    color = "Item Condition"
  ) +
  theme_minimal(base_size = 14) + 
  theme(
    plot.title = element_text(face = "bold", size = 16, margin = margin(b = 10)),
    plot.subtitle = element_text(color = "gray40", size = 11, margin = margin(b = 15)),
    panel.grid.minor = element_blank(),
    legend.position = "bottom"
  )