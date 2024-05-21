import json
import os
import matplotlib.pyplot as plt

def get_grades(subject: str, year: int):
    datas = []
    try:
        with open(os.path.join(f"results", str(year), subject)+'.json', encoding='utf-8') as f:
            datas = json.load(f)
    except FileNotFoundError:
        exit("Nem volt ilyen év vagy tantárgy!")
    grades = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for item in datas:
        current = grades.get(datas[item], 0)
        grades[datas[item]] = int(current) + 1
    return grades

def result_plot(subject: str, year: int):
    grades = get_grades(subject, year)
    fig,ax = plt.subplots()
    ax.bar(grades.keys(), grades.values())
    ax.set_xlabel('Érdemjegy')
    ax.set_ylabel('Darab')
    ax.set_title(f'Eloszlás {year} {subject}')
    maxy = max(grades.values())
    ax.set_xticks([1,2,3,4,5])
    ax.set_yticks(range(maxy+1))
    fig.savefig(f'{subject}_{year}_results.png')

def result_plot_over_years(subjects: list):
    years = os.scandir('results')
    years = [int(year.name) for year in years]
    fig,ax = plt.subplots()
    for subject in subjects:
        x = {}
        for year in years:
            try:
                with open(os.path.join(f"results", str(year), subject)+'.json', encoding='utf-8') as f:
                    datas = json.load(f)
                    grades = get_grades(subject, year)
                    length = len(datas)
                    atment = 0
                    for key, val in grades.items():
                        if key > 1:
                            atment += int(val)
                    for key, val in grades.items():
                        if key > 1:
                            x[year] = int((atment/length)*100)
            except FileNotFoundError:
                x[year] = 0
        
        ax.plot(x.keys(), x.values(), label=subject)
        ax.set_xlabel('Év')
        ax.set_ylabel('Átment százalék')
        ax.set_yticks([0, 20, 40, 60, 80])
        ax.set_xticks(years)
        ax.legend()
    fig.savefig(f'{"_".join(subjects)}_results.png')


def main():
    #result_plot('art',2018)
    result_plot_over_years(['math', 'music'])



if __name__ == '__main__':
    main()