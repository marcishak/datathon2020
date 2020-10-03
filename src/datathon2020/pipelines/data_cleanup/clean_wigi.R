args = commandArgs(trailingOnly=TRUE)

# print(args[1])
path = args[1]
setwd(path)

suppressMessages(library(haven))
suppressMessages(library(dplyr))
suppressMessages(library(tidyr))
suppressMessages(library(readr))

df <- haven::read_dta("wgidataset.dta")
df <- df %>% 
    select(year, ends_with("e"))

write_csv(df, "wgidataset.csv")
