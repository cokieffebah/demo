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

wrap_around("build"){
  sh "ls -lta"
  build()
}
  
wrap_around("scan"){  
  scan()
}

deploy()