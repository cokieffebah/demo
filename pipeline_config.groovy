libraries{
    in_toto_ex{
        in_toto{
            build = [
                "expected_materials": [],
                "expected_products": [["CREATE", "demo-project/*"], ["DISALLOW", "*"]]
            ]
            scan{

            }
            deploy{

            }
        }
    }

    in_toto_utils{
        inside_image = "in-toto-python:demo"

        create_layout {
            extra_skip_libs = ['in_toto_utils']
        }
    }

}

intotoCollector = []