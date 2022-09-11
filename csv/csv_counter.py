import csv

from collections import defaultdict
from datetime import datetime


def read_results_csv(prediction_csv_path: str):
    cat = defaultdict(lambda: 0)
    cat_valid = defaultdict(lambda: 0)
    cat_prob_m = defaultdict(lambda: 0)
    cat_repo = defaultdict(lambda: set())
    any_d_repo = set()
    total_repos = set()
    total = 0

    with open(prediction_csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for line in csv_reader:
            category = line[1]
            prob = float(line[int(category) + 2])

            repo_name = line[0].split('-#-')[0]
            cat_repo[category].add(repo_name)
            total_repos.add(repo_name)
            if category != '0':
                any_d_repo.add(repo_name)

            cat[category] += 1
            total += 1
            cat_prob_m[category] += prob
            if prob > 0.5:
                cat_valid[category] += 1
    for category in sorted(cat.keys()):
        print(
            f'{category}: {cat[category]}, diff {cat[category] - cat_valid[category]}, prob: {cat_prob_m[category] / cat[category]:.4f}, {cat[category] / total * 100:.2f}%, repos: {len(cat_repo[category])} {len(cat_repo[category]) / len(total_repos) * 100:.2f}%')
    print(
        f'Total: {total}, repos: {len(total_repos)}, with diagram {len(any_d_repo)}, {len(any_d_repo) / len(total_repos):.2%}')


def get_csv_reader(csv_path: str):
    csv_file = open(csv_path)

    return csv.reader(csv_file, delimiter=',')


def merge_csv(prediction_csv_path: str, images_csv_path: str, dest_path: str):
    prediction_csv = get_csv_reader(prediction_csv_path)
    images_csv = get_csv_reader(images_csv_path)
    csv_file = open(dest_path, mode='w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Repository', 'Name', 'Category', 'Img last update', 'Repo last update', 'Path'])
    categories = {}
    discarded = 0
    for line in prediction_csv:
        category = line[1]
        categories[line[0]] = category
    for line in images_csv:
        key = f'{line[0]}-#-{line[1]}'
        if key in categories:
            category = categories[key]
            line.insert(2, category)
            csv_writer.writerow(line)
        else:
            discarded += 1
    csv_file.close()
    print(f'Discarded: {discarded}')


def read_merged_csv(csv_path: str):
    cat = defaultdict(lambda: 0)
    cat_date = defaultdict(lambda: 0)
    cat_repo = defaultdict(lambda: set())
    total_repos = set()
    any_diagram_diff = 0
    any_diagram_count = 0
    total = 0
    empty = 0
    header = True

    for line in get_csv_reader(csv_path):
        if header:
            header = False
            continue
        category = line[2]

        repo_name = line[0]
        cat_repo[category].add(repo_name)
        total_repos.add(repo_name)
        if line[3] != '':
            image_date = datetime.fromisoformat(line[3])
            repo_date = datetime.fromisoformat(line[4])
            diff_days = (repo_date - image_date).days
            cat_date[category] += diff_days
            cat[category] += 1
            total += 1
            if category != '0':
                any_diagram_diff += diff_days
                any_diagram_count += 1
        else:
            empty += 1

    for category in sorted(cat.keys()):
        print(f'{category}: {cat[category]}, days: {cat_date[category] / cat[category]}, {cat[category] / total * 100}%, repos: {len(cat_repo[category])}, {len(cat_repo[category]) / len(total_repos) * 100}%')
    print(
        f'Total: {total}, repos: {len(total_repos)}, empty dates: {empty}, any diagram: {any_diagram_count}, any diagram days: {any_diagram_diff / any_diagram_count}')


def main():
    read_results_csv('results.csv')
    merge_csv('results.csv', 'images_on_repositories.csv', 'diagrams_dataset_v2.csv')
    read_merged_csv('diagrams_dataset_v2.csv')


if __name__ == '__main__':
    main()
