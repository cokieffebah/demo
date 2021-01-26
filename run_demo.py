import os
import sys
import shlex
import subprocess
import argparse
import time
from shutil import copyfile, copytree, rmtree

try:
  input = raw_input
except NameError:
  pass

NO_PROMPT = False

def create_layout():
  prompt_key("Define supply chain layout (Alice)")
  os.chdir("owner_alice")
  create_layout_cmd = "python create_layout.py"
  print(create_layout_cmd)
  subprocess.call(shlex.split(create_layout_cmd))
  print('create_layout()')

def package():
  prompt_key("Package (Carl)")
  os.chdir("../functionary_carl")
  package_cmd = ("in-toto-run"
                 " --verbose"
                 " --step-name package --materials demo-project/foo.py demo-project/vcs.log"
                 " --products demo-project.tar.gz"
                 " --key carl --record-streams"
                 " -- tar --exclude '.git' -zcvf demo-project.tar.gz demo-project")
  print(package_cmd)
  subprocess.call(shlex.split(package_cmd))


def create_final_product(directory):
  prompt_key("Create final product")
  os.chdir(directory)
  copyfile("owner_alice/root.layout", "final_product/root.layout")
  copyfile("owner_alice/fetch-upstream.776a00e2.link", "final_product/fetch-upstream.776a00e2.link")
  
  if not os.path.isdir("final_product/fetch-upstream.776a00e2"):
    os.mkdir("final_product/fetch-upstream.776a00e2")
  
  copyfile("functionary_bob/clone.776a00e2.link", "final_product/fetch-upstream.776a00e2/clone.776a00e2.link")
  copyfile("functionary_bob/vcs-log.776a00e2.link", "final_product/fetch-upstream.776a00e2/vcs-log.776a00e2.link")
  copyfile("functionary_bob/update-version.776a00e2.link", "final_product/update-version.776a00e2.link")
  copyfile("functionary_carl/package.2f89b927.link", "final_product/package.2f89b927.link")
  copyfile("functionary_carl/demo-project.tar.gz", "final_product/demo-project.tar.gz")
  print('create_final_product()')

def verify_final_product():
  prompt_key("Verify final product (client)")
  os.chdir("final_product")
  copyfile("../owner_alice/alice.pub", "alice.pub")
  verify_cmd = ("in-toto-verify"
                " --verbose"
                " --layout root.layout"
                " --layout-key alice.pub")
  print(verify_cmd)
  retval = subprocess.call(shlex.split(verify_cmd))
  print("Return value: " + str(retval))  
  print('verify_final_product()')

def prompt_key(prompt):
  if NO_PROMPT:
    print("\n" + prompt)
    return
  inp = False
  while inp != "":
    try:
      inp = input("\n{} -- press any key to continue".format(prompt))
    except Exception:
      pass

def clean():
  files_to_delete = [
    "owner_alice/root.layout",
    "owner_alice/fetch-upstream.776a00e2.link",
    "functionary_bob/clone.776a00e2.link",
    "functionary_bob/vcs-log.776a00e2.link",
    "functionary_bob/update-version.776a00e2.link",
    "functionary_bob/demo-project",
    "functionary_carl/package.2f89b927.link",
    "functionary_carl/demo-project.tar.gz",
    "functionary_carl/demo-project",
    "final_product/alice.pub",
    "final_product/demo-project.tar.gz",
    "final_product/package.2f89b927.link",
    "final_product/fetch-upstream.776a00e2.link",
    "final_product/vcs-log.2f89b927.link",
    "final_product/clone.776a00e2.link",
    "final_product/update-version.776a00e2.link",
    "final_product/untar.link",
    "final_product/root.layout",
    "final_product/fetch-upstream.776a00e2",
    "final_product/demo-project",
  ]

  for path in files_to_delete:
    if os.path.isfile(path):
      os.remove(path)
    elif os.path.isdir(path):
      rmtree(path)


def supply_chain():

  create_layout()

  prompt_key("Clone source code (Bob)")
  os.chdir("../functionary_bob")
  clone_cmd = ("in-toto-run"
                    " --verbose"
                    " --step-name clone --products demo-project/*"
                    " --key bob -- git clone https://github.com/in-toto/demo-project.git")
  print(clone_cmd)
  subprocess.call(shlex.split(clone_cmd))


  prompt_key("Create vcs.log (Bob)")
  os.chdir("../functionary_bob")
  # clone_cmd = ("in-toto-run"
  #                   " --verbose"
  #                   " --step-name vcs-log --products demo-project/vcs.log"
  #                   " --key bob -- git log --pretty=oneline > demo-project/vcs.log")
  # print(clone_cmd)
  log_start_cmd = ("in-toto-record"
                    " start"
                    " --verbose"
                    " --step-name vcs-log"
                    " --key bob")
  print(log_start_cmd)
  subprocess.call(shlex.split(log_start_cmd))

  log_cmd = "git log --pretty=oneline > demo-project/vcs.log"
  print(log_cmd)
  subprocess.call(log_cmd, shell=True)

  log_stop_cmd = ("in-toto-record"
                    " stop"
                    " --verbose"
                    " --step-name vcs-log"
                    " --key bob"
                    " --products demo-project/vcs.log")

  print(log_stop_cmd)
  subprocess.call(shlex.split(log_stop_cmd))




  prompt_key("Update version number (Bob)")
  update_version_start_cmd = ("in-toto-record"
                    " start"
                    " --verbose"
                    " --step-name update-version"
                    " --key bob"
                    " --materials demo-project/vcs.log")

  print(update_version_start_cmd)
  subprocess.call(shlex.split(update_version_start_cmd))

  update_version = "echo 'VERSION = \"foo-v1\"\n\nprint(\"Hello in-toto\")\n' > demo-project/foo.py"
  print(update_version)
  subprocess.call(update_version, shell=True)

  update_version_stop_cmd = ("in-toto-record"
                    " stop"
                    " --verbose"
                    " --step-name update-version"
                    " --key bob"
                    " --products demo-project/foo.py")

  print(update_version_stop_cmd)
  subprocess.call(shlex.split(update_version_stop_cmd))

  copytree("demo-project", "../functionary_carl/demo-project")

  package()
  create_final_product("..")

  prompt_key("Verify final product (client)")
  os.chdir("final_product")
  copyfile("../owner_alice/alice.pub", "alice.pub")
  verify_cmd = ("in-toto-verify"
                " --verbose"
                " --layout root.layout"
                " --layout-key alice.pub")
  print(verify_cmd)
  retval = subprocess.call(shlex.split(verify_cmd))
  print("Return value: " + str(retval))


  prompt_key("Tampering with the supply chain")
  os.chdir("../functionary_carl")
  tamper_cmd = "echo 'something evil' >> demo-project/foo.py"
  print(tamper_cmd)
  subprocess.call(tamper_cmd, shell=True)


  prompt_key("Package (Carl)")
  package_cmd = ("in-toto-run"
                 " --verbose"
                 " --step-name package --materials demo-project/foo.py"
                 " --products demo-project.tar.gz"
                 " --key carl --record-streams"
                 " -- tar --exclude '.git' -zcvf demo-project.tar.gz demo-project")
  print(package_cmd)
  subprocess.call(shlex.split(package_cmd))


  create_final_product("..")


  prompt_key("Verify final product (client)")
  os.chdir("final_product")
  copyfile("../owner_alice/alice.pub", "alice.pub")
  verify_cmd = ("in-toto-verify"
                " --verbose"
                " --layout root.layout"
                " --layout-key alice.pub")

  print(verify_cmd)
  retval = subprocess.call(shlex.split(verify_cmd))
  print("Return value: " + str(retval))


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-n", "--no-prompt", help="No prompt.",
      action="store_true")
  parser.add_argument("-c", "--clean", help="Remove files created during demo.",
      action="store_true")
  parser.add_argument("-f", "--fresh", help="Remove files created during demo. then run",
      action="store_true")    


  args = parser.parse_args()

  if args.clean:
    clean()
    sys.exit(0)

  if args.no_prompt:
    global NO_PROMPT
    NO_PROMPT = True

  if args.fresh:
    clean()

  supply_chain()

if __name__ == '__main__':
  main()
