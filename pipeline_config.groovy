libraries{
    in_toto_ex{
        in_toto{
            build{ 
                record{
                    materials = []
                    products = "demo-project/*"
                    key = "func"
                }
                
                layout{
                    materials = []
                    products = [["CREATE", "demo-project/*"], ["DISALLOW", "*"]]
                }
            }
            scan{
                record{
                    materials = "demo-project/*"
                    products = "scan.log"
                    key = "func"
                }
                layout{
                    materials = [["MATCH", "demo-project/*", "WITH", "PRODUCTS", "FROM", "build"]]
                    products = [["CREATE", "scan.log"], ["DISALLOW", "*"]]
                }
            }
            
            package_app{
                layout{
                    materials =  [
                    ["MATCH", "demo-project/*", "WITH", "PRODUCTS", "FROM", "build"], 
                    ["MATCH", "scan.log", "WITH", "PRODUCTS", "FROM", "scan"], ["DISALLOW", "*"]]

                    products = [["CREATE", "demo-project.tar.gz"], ["DISALLOW", "*"]]
                }
                record{
                    key = "func"
                    materials =  "demo-project/* scan.log"
                    products = "demo-project.tar.gz"
                }
            }
            deploy{}
        }
    }

    in_toto_utils{
        inside_image = "in-toto-python:demo"
        functionary{
            path = "func"
            generate = true
        }

        layout{
            signer = "func"
            generate = false
        }
    }

}