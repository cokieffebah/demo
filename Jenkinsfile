node{
    cleanWs()
    try{
        checkout scm
    }catch(hudson.AbortException ex) {
        println "scm var not present, skipping source code checkout" 
    }catch(err){
        println "exception ${err}" 
    } 
    
    stash name: 'workspace', allowEmpty: true, useDefaultExcludes: false
}

intoto_record("build"){
  sh "ls -lta"
  build()
}
  
intoto_record("scan"){  
  scan()
}

intoto_record("package_app"){  
  package_app()
}

porter_utils.image_wrap {
  sh(script:"~/.porter/porter create")
  sh(script:"docker build -t intoto-demo:latest -f porter/porter.Dockerfile .")
  sh(script:"docker image tag intoto-demo:latest localhost:5000/intoto-demo:latest")
  def sh_status = sh(returnStatus: true, script:"DOCKER_CONTENT_TRUST_ROOT_PASSPHRASE='phrase' DOCKER_CONTENT_TRUST_REPOSITORY_PASSPHRASE='phrase' DOCKER_CONTENT_TRUST=1 DOCKER_CONTENT_TRUST_SERVER=https://192.168.1.196:4443 docker -D push localhost:5000/intoto-demo:latest") 
  
  deploy()
}
