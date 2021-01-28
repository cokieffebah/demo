import os
import sys
import shlex
import subprocess
import argparse
import time
import json
from shutil import copyfile, copytree, rmtree

# import the owner_alice/create_layout
sys.path.append(os.getcwd() + "/owner_alice")
import create_layout as alice_layout


try:
  input = raw_input
except NameError:
  pass

NO_PROMPT = False

def create_layout(config_json=None):
  
  prompt_key("Define supply chain layout (Alice)")
  os.chdir("owner_alice")
  
  # another way to import owner_alice/create_layout
  #import importlib.util
  #spec = importlib.util.spec_from_file_location("alice.create_layout", os.getcwd() + "/create_layout.py")
  #alice_layout = importlib.util.module_from_spec(spec)
  #spec.loader.exec_module(alice_layout)

  if not config_json:
    alice_layout.main()
  else:  
    alice_layout.create_layouts(config_json)

  # previously was another python shell call
  #create_layout_cmd = "python create_layout.py"
  #print(create_layout_cmd)
  #subprocess.call(shlex.split(create_layout_cmd))
  
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
  print('package()')


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
  json_file = './jte/in-toto.json'

  with open(json_file) as f:
    read_data = f.read()
    print('in-toto.json: ' + read_data)
    config_json = json.loads(read_data)

  create_layout(config_json)

  prompt_key("Clone source code (Bob)")
  os.chdir("../functionary_bob")
  step_name = "clone"
  current_json = config_json["named"][step_name]
  clone_cmd = ("in-toto-run"
                    " --verbose"
                    " --step-name {} --products {}"
                    " --key bob -- git clone https://github.com/in-toto/demo-project.git"
              ).format(step_name, current_json["expected_products"][0][1])
  print(clone_cmd)
  subprocess.call(shlex.split(clone_cmd))


  prompt_key("Create vcs.log (Bob)")
  step_name = "vcs-log"
  current_json = config_json["named"][step_name]
  os.chdir("../functionary_bob")
  # clone_cmd = ("in-toto-run"
  #                   " --verbose"
  #                   " --step-name vcs-log --products demo-project/vcs.log"
  #                   " --key bob -- git log --pretty=oneline > demo-project/vcs.log")
  # print(clone_cmd)
  log_start_cmd = ("in-toto-record"
                    " start"
                    " --verbose"
                    " --step-name {}"
                    " --materials {}"
                    " --key bob"
                    ).format(step_name, current_json["expected_materials"][0][1])
  print(log_start_cmd)
  subprocess.call(shlex.split(log_start_cmd))

  log_cmd = "git log --pretty=oneline > demo-project/vcs.log"
  print(log_cmd)
  subprocess.call(log_cmd, shell=True)

  log_stop_cmd = ("in-toto-record"
                    " stop"
                    " --verbose"
                    " --step-name {}"
                    " --key bob"
                    " --products {}"
                    ).format(step_name, current_json["expected_products"][0][1])

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
  parser.add_argument("-f", "--fresh", help="Remove files previously created during demo. then run",
      action="store_true") 
  parser.add_argument("-t", "--test", help="run test section then exit",
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

  if args.test:
    create_layout()
    sys.exit(0)  

  supply_chain()

if __name__ == '__main__':
  main()
