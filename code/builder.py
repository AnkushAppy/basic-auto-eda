import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set()


class ReportBuilder:
    def __init__(self, data=None, file_path=None):
        self.categorical_columns = []
        self.numerical_columns = []
        if data is not None:
            self.data = data
            self.set_categorical_columns()
            self.set_numerical_columns()
        if file_path:
            self.read_csv(file_path)


    def read_csv(self, file_path=None):
        self.data = pd.read_csv(file_path, encoding='iso-8859-1')
        self.set_categorical_columns()
        self.set_numerical_columns()

    def set_categorical_columns(self):
        self.categorical_columns = self.data.dtypes[self.data.dtypes == 'object'].index

    def set_numerical_columns(self):
        self.numerical_columns = self.data.dtypes[self.data.dtypes != 'object'].index

    def convert_this_to_categorical_columns(self, numerical_cols=None):
        for col in numerical_cols:
            self.data[col] = self.data[col].astype('object')
        self.set_categorical_columns()
        self.set_numerical_columns()

    def remove_this_from_categorical(self, remove_cols=None):
        return list(set(self.categorical_columns) - set(remove_cols))

    def get_unique_narratives(self, col=None):
        val = self.data[col].value_counts()
        text = "This are unique values in this categorical column. "
        unique_values = val.index
        unique_values = [str(i) for i in unique_values]
        text = text + " ,".join(unique_values)
        return text

    def get_top_5_on_categorical(self, col=None):
        val = self.data[col].value_counts()
        text = "Top values are:"
        text_val = ["{0} ({1}),".format(val.index[i], val.values[i]) for i in range(5 if len(val) > 5 else len(val))]
        return (text, text_val)

    def get_statistical_narratives(self, col=None):
        col_desc = self.data[col].describe()
        text = "Stats:"
        text_val = ["{0} ({1})".format(col_desc.index[i], col_desc.values[i]) for i in range(len(col_desc))]
        return (text, text_val)

    def quantile_cal(self, df=None, target_col='', count_col=''):
        if df is None:
            df = self.data
        new_df = df[[target_col, count_col]]
        sum_new_df = new_df[count_col].sum()
        new_df['percentile'] = new_df[count_col] / sum_new_df
        new_df = new_df.sort_values('percentile', ascending=False)
        return new_df

    def quantile_cal_cat(self, df=None, target_col=''):
        if df is None:
            df = self.data
        new_df = df[target_col].value_counts()
        sum_new_df = pd.DataFrame()
        sum_new_df[target_col] = new_df.index
        sum_new_df['values'] = new_df.values
        sum_new_df['percentile'] = sum_new_df['values'] * 100 / new_df.sum()
        sum_new_df = sum_new_df.sort_values('percentile', ascending=False)
        return sum_new_df

    def get_this_percentile(self, df=None, perc=50):
        names = []
        percentages = []
        percent_sum = 0
        for i in df.T:
            if percent_sum < perc:
                percent_sum += df.T[i].percentile
                names.append(df.T[i][0])
                percentages.append(df.T[i][2])
        return names, percentages, percent_sum

    def get_this_percentile_bottom(self, df=None, perc=20):
        df = df.sort_values('percentile', ascending=True)
        names = []
        percentages = []
        percent_sum = 0
        for i in df.T:
            if percent_sum < perc:
                percent_sum += df.T[i].percentile
                names.append(df.T[i][0])
                percentages.append(df.T[i][2])
        return names, percentages, percent_sum
