
build()
scan()
deploy()

println "pipelineConfig.intotoCollector: ${pipelineConfig.intotoCollector}"
pipelineConfig.intotoCollector.each{ c ->
    println "for ${c}: pipelineConfig.libraries[${c.library}].in_toto[${c.step}]: ${pipelineConfig.libraries[c.library].in_toto[c.step]}"
}