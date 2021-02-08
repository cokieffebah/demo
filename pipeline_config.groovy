libraries{
    in_toto_ex{
        in_toto{
            build{ 
                materials = []
                products = [["CREATE", "demo-project/*"], ["DISALLOW", "*"]]
                key = "functionary_bob/bob"
            }
            scan{
                materials = [["ALLOW", "demo-project/*"]]
                products = [["ALLOW", "demo-project/*"], ["DISALLOW", "*"]]
                key = "functionary_bob/bob"
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