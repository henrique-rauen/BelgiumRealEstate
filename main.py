#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
#Last Modified: 2023-07-05 10:32
import utils.utils as u

df = u.clean_df("data.csv")
print(df)
df.to_csv("teste_data.csv",index=False)
