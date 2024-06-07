import matplotlib.pyplot as plt
import seaborn as sns


def plot_salaries(df):
    """
    Строит график зарплат.
    """
    plt.figure(figsize=(12, 5))
    sns.set(style="whitegrid")

    for index, row in df.iterrows():
        plt.plot([row['min'], row['max']], [index, index], 'o-', color='red')
        plt.scatter(row['mean'], index, color='blue', zorder=3)

    plt.yticks(range(len(df)), df['position'])
    plt.gca().invert_yaxis()
    plt.xlabel('Зарплата (тыс. рублей)')
    plt.title('Анализ зарплат')
    plt.show()


if __name__ == '__main__':
    pass
