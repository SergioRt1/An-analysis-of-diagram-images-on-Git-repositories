import csv
import os
import shutil
from pathlib import Path

from git import Repo, GitCommandError
from tqdm import tqdm

import constants
from image_extractor import ImageExtractor

extractors = [ImageExtractor]


def map_repo_name(name):
    if name[-1] == '/':
        name = name[:-1]
    return name.replace('/', '_')


def is_valid_row(number: str):
    return int(number) > 0


def get_repos(use_gh_torrent: bool, limit: int):
    repos = {}
    if use_gh_torrent:
        path = constants.GHTorrent_projects_path
    else:
        path = constants.external_dataset_path

    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, )
        is_header = True
        for row in csv_reader:
            if is_header:
                is_header = False
            else:
                if len(row) > 3:
                    if use_gh_torrent:
                        name = row[3]
                        repos[name] = row[1].replace('api.', '').replace('/repos', '')
                    else:
                        if is_valid_row(row[6]) or is_valid_row(row[7]) or is_valid_row(row[9]):
                            name = map_repo_name(row[0])
                            repos[name] = row[1]
            if len(repos) >= limit:
                break
    return repos


def extract_data(repo_name: str, repo, dataset_writer):
    if not os.path.exists(constants.dataset_dir):
        os.mkdir(constants.dataset_dir)
    try:
        for extractor in extractors:
            file_paths = (p.resolve() for p in Path(repo.working_dir).glob("**/*") if
                          p.suffix in extractor.valid_extensions)
            for file_path in file_paths:
                if extractor.is_valid(file_path):
                    shutil.copy(file_path, os.path.join(constants.dataset_dir, f'{repo_name}-#-{file_path.name}'))
                    last_modification = repo.git.log('-1', '--pretty="%cI"', file_path).strip('"')
                    full_path = str(file_path.relative_to(repo.working_dir))
                    dataset_writer.writerow(
                        [repo_name, file_path.name, last_modification, repo.head.commit.authored_datetime.isoformat(), full_path]
                    )
    finally:
        shutil.rmtree(repo.working_dir, ignore_errors=True)


def main(target_csv_path: str):
    os.chdir('../')

    if not os.path.exists(constants.repos_dir):
        os.makedirs(constants.repos_dir)

    current_repos = set(os.listdir(constants.repos_dir))
    with open(target_csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            current_repos.add(row[0])

    repos = get_repos(True, 550_000)
    print('Current repos:', len(current_repos))
    downloaded_repos = 287201
    start_from = 510068

    with open(target_csv_path, 'a', newline='') as dataset_metadata_file:
        dataset_metadata = csv.writer(dataset_metadata_file)
        with open('csv/count.txt', 'w') as downloaded_count:
            counter = 0
            for repo_name in tqdm(repos):
                counter += 1
                if counter < start_from:
                    continue
                try:
                    repo_path = os.path.join(constants.repos_dir, repo_name)
                    if repo_name not in current_repos:
                        repo_url = repos[repo_name]
                        repo = Repo.clone_from(repo_url, repo_path)
                        extract_data(repo_name, repo, dataset_metadata)
                    downloaded_repos += 1
                    downloaded_count.write(f'{downloaded_repos}\n')
                    downloaded_count.flush()
                except GitCommandError:
                    pass
                except Exception as e:
                    print('Unknown exception:', e)
                except:
                    print('Downloaded repos:', downloaded_repos)
    print('Downloaded repos:', downloaded_repos)


main('csv/images_on_repositories.csv')