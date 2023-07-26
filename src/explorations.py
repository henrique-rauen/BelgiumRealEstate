#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
from . import plot_funcs as p
from . import utils as u
if __name__ == "__main__":
    df = u.clean_df("../data/data.csv")
    df_no_outliers = p.outliers(df)
    plot(df_no_outliers)

def plot(df_no_outliers):
    p.hist_living(df_no_outliers)
    p.per_province(df_no_outliers)
    p.square_meter_per_province(df_no_outliers)
    p.map(df_no_outliers)
    p.numeric_corr(df_no_outliers)
    p.cat_corr(df_no_outliers)
    p.localities_count(df_no_outliers)
    p.cities_count(df_no_outliers)
    p.cities_corr(df_no_outliers)
    p.cat_corr_city(df_no_outliers)
