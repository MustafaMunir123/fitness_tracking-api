from typing import Dict


class UserDetailServices:

    @staticmethod
    def copy_to_initial_data(data: Dict) -> None:
        data.update(
            {
                "ini_height": data["height"],
                "ini_weight": data["weight"],
                "ini_sleep": data["sleep"],
                "ini_walk": data["walk"]
            }
        )
