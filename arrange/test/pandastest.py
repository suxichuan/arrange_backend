import pandas as pd


df=pd.read_excel('人员信息模板.xlsx')
print(df.index)
# try:
#     for i in range(0,int(df.size)-2):
#         print(i)
        # print(df.loc[i]['处理时间'])
# except Exception as e:
#     print(e)
# for i in df.iterrows():3
#     print(i)
#     break

# for i in df.index:
#     print(df.loc[i]['人员编码'])