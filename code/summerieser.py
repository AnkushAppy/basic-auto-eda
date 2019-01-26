import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set()
from code.reporter import CreateReport
from code.builder import ReportBuilder
from code.settings import DATA_PATH, DEAULT_CHART_SIZE, FILE_NAME, REPORT_FILE_NAME


def add_heading_to_report(text='', size=2, tab_after_text=1):
    cr.add_header(text, size)
    for _ in range(tab_after_text):
        cr.add_space()


def add_categorical_text(cr, rb, col):
    cr.add_paragraph(col)
    text_para = rb.get_unique_narratives(col)
    value_para = rb.get_top_5_on_categorical(col)
    cr.add_paragraph(text_para)
    cr.add_bullets(*value_para)


def add_cat_plot(cr, rb, i, graph_type):
    add_categorical_text(cr, rb, i)

    if graph_type == 'count_plot':
        plt.figure(i, figsize=DEAULT_CHART_SIZE)
        sns_plot = sns.countplot(i, data=rb.data, order=rb.data[i].value_counts().index)
        plt.xticks(rotation=45)
        image_path, image_name = cr.get_image_path(graph_type, i)
        sns_plot.figure.savefig(image_path)
        cr.add_plot(file_name=image_name, text=image_path)


def add_basic_categorical_details(cr, rb, remove_this):
    add_heading_to_report('Categorical Variables')

    graph_type = 'count_plot'
    categorical_columns = rb.remove_this_from_categorical(remove_cols=remove_this)
    for i in categorical_columns:
        add_cat_plot(cr, rb, i, graph_type)


def add_num_text(cr, rb, i):
    cr.add_paragraph(i)
    value_para = rb.get_statistical_narratives(i)
    cr.add_bullets(*value_para)


def add_num_plot(cr, rb, i, graph_type):
    plt.figure(i)
    image_path, image_name = cr.get_image_path(graph_type, i)

    if graph_type == 'dist_plot':
        sns_plot = sns.distplot(rb.data[i])
        sns_plot.figure.savefig(image_path)

    elif graph_type == 'violin_plot':
        sns_plot = sns.violinplot(x=rb.data[i])
        sns_plot.figure.savefig(image_path)

    elif graph_type == 'box_plot':
        sns_plot = sns.boxplot(x=rb.data[i])
        sns_plot.figure.savefig(image_path)

    cr.add_plot(file_name=image_name, text=image_path)
    plt.clf()


def add_basic_numerical_details(cr, rb):
    add_heading_to_report('Numerical Variables')

    numerical_columns = rb.numerical_columns
    for i in numerical_columns:
        add_num_text(cr, rb, i)

        graph_type = 'dist_plot'
        add_num_plot(cr, rb, i, graph_type)

        graph_type = 'violin_plot'
        add_num_plot(cr, rb, i, graph_type)

        graph_type = 'box_plot'
        add_num_plot(cr, rb, i, graph_type)


def add_relplot(cr, rb, i, target_column, graph_type):

    image_path, image_name = cr.get_image_path(graph_type, target_column + "_vs_" + i)
    plt.figure(i)
    sns_plot = sns.relplot(x=target_column, y=i, data=rb.data)
    sns_plot.savefig(image_path)
    cr.add_plot(file_name=image_name, text=image_path)
    plt.clf()


def add_basic_target_vs_numerical(cr, rb, target_column):
    add_heading_to_report('Target vs Numerical')

    for i in rb.numerical_columns:
        cr.add_paragraph(i)
        graph_type = "relplot"
        add_relplot(cr, rb, i, target_column, graph_type)


def add_basic_target_vs_categorical(cr, rb, target_column, remove_cols=None):
    add_heading_to_report('Target vs Categorical')
    categorical_colums = rb.remove_this_from_categorical(remove_cols=remove_cols)
    for i in categorical_colums:
        if i == target_column:
            continue
        cr.add_paragraph(i)
        graph_type = 'count_plot'
        plt.figure(i, figsize=(15, 8))
        sns_plot = sns.countplot(i, data=rb.data, hue=target_column, order=rb.data[i].value_counts().index)
        plt.xticks(rotation=45)
        image_path, image_name = cr.get_image_path(graph_type, target_column + "_vs_" + i)
        sns_plot.figure.savefig(image_path)
        cr.add_plot(file_name=image_name, text=image_path)
        plt.clf()


data_path = DATA_PATH + FILE_NAME
report_file_name = REPORT_FILE_NAME  # type: str


cr = CreateReport(report_file_name)
rb = ReportBuilder(file_path=data_path)

remove_from_categorical = []
convert_these_to_categorical = []

rb.convert_this_to_categorical_columns(numerical_cols=convert_these_to_categorical)
rb.remove_this_from_categorical(remove_cols=remove_from_categorical)

add_basic_categorical_details(cr, rb, remove_this=remove_from_categorical)

add_basic_numerical_details(cr, rb)

target_column: str = 'target' # str : name of the target column in dataset

add_basic_target_vs_numerical(cr, rb, target_column)
add_basic_target_vs_categorical(cr, rb, target_column, remove_cols=remove_from_categorical)

cr.close()
