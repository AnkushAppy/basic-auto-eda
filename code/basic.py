#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set()

file_path = "adult.csv"
target_column = 'target'
report_file_name = 'report.md'
df = pd.read_csv(file_path)
df.head()

import os
import sys

class CreateReport:
    
    def __init__(self, file_name=None):
        if file_name is not None:
            if file_name[-3:] == ".md":
                pass
            else:
                file_name = file_name + ".md"
        else:
            raise("File name not given")
        self.fp = open(file_name, 'w+')

    def get_report_file(self):
        return self.fp

    def add_header(self, header="Header", size=4):
        header = "#"*size + " " + header
        self.fp.write(header)
        self.add_space()
        self.add_space()

    def add_paragraph(self, paragraph="paragraph"):
        self.fp.write(paragraph)
        self.add_space()
        self.add_space()
        
    def add_bullets(self, text=None, values_text=None):
        self.fp.write(text)
        self.add_space()
        for i in values_text:
            bullet = "* " + i
            self.fp.write(bullet)
            self.add_space()
        self.add_space()
        self.add_space()
    
    def add_space(self):
        self.fp.write('\n')

    def add_plot(self, file_name="", text=""):
        image_text = "![{0}]({1})".format(text, file_name)
        self.fp.write(image_text)
        self.add_space()
        self.add_space()
        
    def add_code():
        pass
    
    def close(self):
        self.fp.close()



class ReportBuilder:
    def __init__(self, data=None):
        self.data = df
        self.categorical_columns = []
        self.numerical_columns = []
        
    def get_unique_narratives(self, col=None):
        val = self.data[col].value_counts()
        text = "This are unique values in this categorical column. "
        unique_values = val.index
        text = text + " ,".join(unique_values)
        return text
    
    def get_top_5_on_categorical(self, col=None):
        val = self.data[col].value_counts()
        text = "Top values are:"
        text_val = ["{0} ({1}),".format(val.index[i],val.values[i]) for i in range( 5 if len(val) > 5 else len(val))]
        return (text,text_val)
    
    def get_statistical_narratives(self, col=None):
        col_desc = self.data[col].describe()
        text = "Stats:"
        text_val = ["{0} ({1})".format(col_desc.index[i],col_desc.values[i]) for i in range(len(col_desc))]
        return (text, text_val)
        

cr = CreateReport(report_file_name)
rb = ReportBuilder(data=df)


# ### Categorical Variables
# Ploting count values of individual categorical columns


cr.add_header('Categorical Variables', 2)
cr.add_space()


categorical_columns = df.dtypes[df.dtypes == 'object'].index
numerical_columns = df.dtypes[df.dtypes != 'object'].index


graph_type = 'count_plot'
for i in categorical_columns:
    cr.add_paragraph(i)
    text_para = rb.get_unique_narratives(i)
    value_para = rb.get_top_5_on_categorical(i)
    cr.add_paragraph(text_para)
    cr.add_bullets(*value_para)
    plt.figure(i, figsize=(15,8))
    sns_plot = sns.countplot(i, data=df, order=df[i].value_counts().index)
    plt.xticks(rotation=45)
    image_path = "{0}_{1}.png".format(graph_type,i)
    sns_plot.figure.savefig(image_path)
    cr.add_plot(file_name=image_path, text=image_path)


# ### Numerical value
# Plotting distribution chart for numerical columns


cr.add_header('Numerical Variables', 2)
cr.add_space()

for i in numerical_columns:
    cr.add_paragraph(i)
    value_para = rb.get_statistical_narratives(i)
    cr.add_bullets(*value_para)
    plt.figure(i)
    graph_type = 'dist_plot'
    sns_plot = sns.distplot(df[i])
    image_path = "{0}_{1}.png".format(graph_type,i)
    sns_plot.figure.savefig(image_path)
    cr.add_plot(file_name=image_path, text=image_path)
    plt.clf()
    plt.figure(i)
    graph_type = 'violin_plot'
    sns_plot = sns.violinplot(x=df[i])
    image_path = "{0}_{1}.png".format(graph_type,i)
    sns_plot.figure.savefig(image_path)
    cr.add_plot(file_name=image_path, text=image_path)
    plt.clf()
    plt.figure(i)
    graph_type = 'box_plot'
    sns_plot = sns.boxplot(x=df[i])
    image_path = "{0}_{1}.png".format(graph_type,i)
    sns_plot.figure.savefig(image_path)
    cr.add_plot(file_name=image_path, text=image_path)


if df[target_column].dtype == 'object':

    cr.add_header('Numerical Column vs Categorical Column', 2)
    cr.add_space()
    for i in numerical_columns:
        cr.add_paragraph(i + " Vs " + target_column)
        plt.figure(i)
        graph_type = 'scatter_plot'
        sns_plot = sns.relplot(x=target_column, y=i, data=df)
        image_path = "{0}_{1}.png".format(graph_type,i)
        sns_plot.savefig(image_path)
        cr.add_plot(file_name=image_path, text=image_path)



	### Numerical Column vs Numerical Columns
    cr.add_header('Numerical Column vs Numerical Column', 2)
    cr.add_space()
    plt.figure(i)
    graph_type = 'pair_plot'
    sns_plot = sns.pairplot(data=df)
    image_path = "{0}_{1}.png".format(graph_type,i)
    sns_plot.savefig(image_path)
    cr.add_plot(file_name=image_path, text=image_path)



    cr.add_header('Numerical Column vs Numerical Column with target column', 2)
    cr.add_space()
    plt.figure(i)
    graph_type = 'pair_plot_with_hue'
    sns_plot = sns.pairplot(data=df, hue='target')
    image_path = "{0}_{1}.png".format(graph_type,i)
    sns_plot.savefig(image_path)
    cr.add_plot(file_name=image_path, text=image_path)

	

	# ### target column vs Categorical Column
	# Ploting count plot on target column vs other categorical columns

    cr.add_header('Target Column vs Categorical Column', 2)
    cr.add_space()

    for i in categorical_columns:
        if i == target_column:
            continue
        cr.add_paragraph(i + " Vs " + target_column)
        graph_type = 'count_plot_with_hue'
        plt.figure(i, figsize=(15,8))
        sns_plot = sns.countplot(i, data=df, hue=target_column, order=df[i].value_counts().index)
        plt.xticks(rotation=45)
        image_path = "{0}_{1}.png".format(graph_type,i)
        sns_plot.figure.savefig(image_path)
        cr.add_plot(file_name=image_path, text=image_path)
else:
    
    ### Numerical Column vs Numerical Columns
    cr.add_header('Numerical Column vs Numerical Column', 2)
    cr.add_space()
    plt.figure(i)
    graph_type = 'pair_plot'
    sns_plot = sns.pairplot(data=df)
    image_path = "{0}_{1}.png".format(graph_type,i)
    sns_plot.savefig(image_path)
    cr.add_plot(file_name=image_path, text=image_path)

    cr.add_header('Target Column vs Categorical Column', 2)
    cr.add_space()

    for i in categorical_columns:
        cr.add_paragraph(i + " Vs " + target_column)
        graph_type = 'count_plot_with_hue'
        plt.figure(i, figsize=(15,8))
        sns_plot = sns.barplot(x=i, y=target_column, data=df)
        plt.xticks(rotation=45)
        image_path = "{0}_{1}.png".format(graph_type,i)
        sns_plot.savefig(image_path)
        cr.add_plot(file_name=image_path, text=image_path)

cr.close()





