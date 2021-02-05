libraries{
    in_toto_ex{
        in_toto{
            build{ 
                expected_materials = []
                expected_products = [["CREATE", "demo-project/*"], ["DISALLOW", "*"]]
            }
            scan{
                expected_materials = []
                expected_products = [["CREATE", "demo-project/*"], ["DISALLOW", "*"]]
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