import os
import sys
import re
import urllib

def get_script_location():
  return os.path.dirname(os.path.realpath(sys.argv[0]))

def make_dirs():
    try:
        os.makedirs(os.path.join(get_script_location(), 'gitDLdFiles'))
    except OSError:
        pass
    
def get_patch_file(__repo_url, commit_hash):
    http_patch_file = urllib.urlopen(__repo_url + commit_hash + '.patch')
    return http_patch_file.read()

def extract_paths(patch_file):
    paths = re.findall(r'(?:diff --git a)(/.*?\.[\S]+)', patch_file)
    return paths

def download_git_commit_file(raw_githubusercontent_repo, commit_hash, path):
        save_path = get_script_location() + '/gitDLdFiles' + path.rpartition('/')[0]
        save_name = path.rpartition('/')[-1]
        try:
            os.makedirs(save_path)
            committed_file = urllib.URLopener()
            committed_file.retrieve(raw_githubusercontent_repo + commit_hash + path, os.path.join(save_path, save_name))
        except OSError:
            committed_file = urllib.URLopener()
            committed_file.retrieve(raw_githubusercontent_repo + commit_hash + path, os.path.join(save_path, save_name))

def main():
    make_dirs()
    git_owner = raw_input('Enter the OWNER: ')
    git_repo = raw_input('Enter the REPO: ')
    commit_hash = raw_input('Enter the COMMIT: ')
    repo_url = 'https://github.com/' + git_owner + '/' + git_repo + '/commit/'
    patch_file = get_patch_file(repo_url, commit_hash)

    paths = extract_paths(patch_file)

    for path in paths:
        print ('https://raw.githubusercontent.com/' + git_owner + '/' + git_repo + '/' + commit_hash + path)
        download_git_commit_file('https://raw.githubusercontent.com/' + git_owner + '/' + git_repo + '/', commit_hash, path)

main()
