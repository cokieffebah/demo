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
  sh("~/.porter/porter create")
  sh("docker build -t intoto-demo:latest -f porter/porter.Dockerfile .")
  sh("DOCKER_CONTENT_TRUST=1 DOCKER_CONTENT_TRUST_SERVER=https://localhost:4443 docker -D push localhost:5000/intoto-demo:latest") 
  deploy()
}
