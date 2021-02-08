libraries{
    in_toto_ex{
        in_toto{
            build{ 
                materials = []
                products = [["CREATE", "demo-project/*"], ["DISALLOW", "*"]]
                key = "functionary_bob/bob"
            }
            scan{
                materials = [["MATCH", "demo-project/*", "WITH", "PRODUCTS", "FROM", "build"]]
                products = [["CREATE", "scan.log"], ["DISALLOW", "*"]]
                key = "functionary_bob/bob"
            }
            
            package{
                // materials =  [
                //     ["MATCH", "demo-project/*", "WITH", "PRODUCTS", "FROM", "build"], 
                //     ["MATCH", "scan.log", "WITH", "PRODUCTS", "FROM", "scan"], ["DISALLOW", "*"]]

                // products = [["CREATE", "demo-project.tar.gz"], ["DISALLOW", "*"]]
                // key = "functionary_carl/carl"
            }
            deploy{}
        }
    }

    in_toto_utils{
        inside_image = "in-toto-python:demo"

        collector {

        }

        create_layout {
            
        }
    }

}