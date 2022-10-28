"""
Recipe manager / portion calculator for custom recipes
"""

import json


class Recipe:
    name = ""
    target_base_portions = int()
    category = ""
    ingredients = []
    instructions = ""
    recipes = {}
    recipe_file = "recipes.txt"

    def __init__(self, name, target_base_portions):
        """
        Load recipe list stored as text file
        """

        self.name = name

        print("\n---------------Recipe Manager------------------")
        print("Loading stored recipes from file \"{}\"...".format(self.recipe_file))
        with open(self.recipe_file) as f:
            self.recipes = json.load(f)

        exists = False
        for recipe in self.recipes:
            if recipe["name"] == name:
                # Recipe already part of list
                print("Chosen recipe is part of the list")

                self.portions = int(recipe["portions"])
                self.category = recipe["category"]
                #  [int(x) for x in recipe["ingredients"] if x.isnumeric()]    # TODO
                self.ingredients = recipe["ingredients"]
                self.instructions = recipe["instructions"]

                self.print_recipe(self, target_base_portions)  # TODO
                exists = True
                break

        if not exists:
            self.target_base_portions = target_base_portions
            self.add_new_recipe()

    def add_new_recipe(self):
        """ Add new recipe to local recipe list stored in .txt file

        data = {
            name: "Pfannkuchen",
            base_portions: 4,
            category: "Suesspeisse",
            ingredients: [ ("Eier", 4), ("Mehl", 150, "g"), ("Milch", 100, "ml") ],
            instructions: "Ruehr alles zusammen und brate alles in der Pfanne ordentlich an :D"
            }
        """
        print("Recipe with name \"{}\" not found in stored recipes".format(self.name))
        print("Adding new recipe ...")

        name = self.name
        target_base_portions = self.target_base_portions

        # Add category, e.g. "Kuchen"
        while True:
            ui_category = input("Input category and confirm with \"Enter\":")  # "ui" == user input
            # Validate entered data
            if not ui_category.isalpha():
                print("Input not viable, please use only alphabet letters (a-z).")
                continue
            else:
                self.category = ui_category
                break

        # Add for ingredients
        add_ingredient = True

        while add_ingredient:
            ui_ingredient_question = input("Add ingredient [\"Y|N\"]?")  # "ui" == user input

            if ui_ingredient_question.lower() == "y":
                ui_ingredient = input("Specify ingredient (e.g. \"flour\"):")

                if not ui_ingredient.isalpha():
                    print("Input not viable, please use only alphabet letters (a-z).")
                    continue
                else:
                    ui_quantities = input("Specify quantity amount comma-separated if weight e.g. \"400,g\" or \"4\"")

                    if "," in ui_quantities:
                        ui_quantities = [x.strip() for x in ui_quantities.split(",")]

                        if len(ui_quantities) > 2:
                            print("Only 2 comma separated values allowed. Please try again.")
                            continue
                        if not (ui_quantities[0].isnumeric() and ui_quantities[1].isalpha()):
                            print("Input not viable, please use only alphanumeric values (a-z, 0-9).")
                            continue
                    else:
                        if not ui_quantities.isalnum():
                            print("Input not viable, please use only alphanumeric values (a-z, 0-9).")
                            continue
                        else:
                            ui_quantities = ui_quantities.strip()

                    res_ingredients = [ui_ingredient]

                    if isinstance(ui_quantities, str):  # e.g. ui_quantities: ["42"] --> str | no weight parameter/unit
                        res_ingredients.extend([ui_quantities])
                        print("{}, {} added to recipe".format(ui_ingredient, ui_quantities))
                    else:   # e.g. ui_quantities: ["1500", "ml"] --> list
                        res_ingredients.extend(ui_quantities)
                        print("{}, {} {} added to recipe".format(ui_ingredient, ui_quantities[0], ui_quantities[1]))

                    self.ingredients.append(res_ingredients)

            else:  # [N]
                add_ingredient = False

        # Add instructions
        add_instructions = True

        while add_instructions:
            ui_instruction = input("Input instructions")
            if ui_instruction:  # TODO
                self.instructions = ui_instruction
                add_instructions = False

        #   Update textfile
        self.recipes.append({
            "name": self.name,
            "category": self.category,
            "portions": self.target_base_portions,
            "ingredients": self.ingredients,
            "instructions": self.instructions
        })

        self.update()

    def print_recipe(self, recipe):
        """ Print recipe for specified portions """
        # TODO
        multiplier = self.target_base_portions / self.portions
        ingredients = [ingredient[1] * multiplier for ingredient in self.ingredients]

        print("Recipe: {} for {} portions".format(self.name, self.target_base_portions))

        for ingredient, count in enumerate(ingredients):
            print("{}: {} ".format(count, " ".join(ingredient)))
        print("Instructions: {}".format(self.instructions))

    def print_recipe_list(self):
        # TODO
        """ Print all recipes stored in .txt file """
        pass

    def get_recipe(self):
        if self.name in self.recipes:
            # TODO
            pass
        else:
            print("Recipe with name {} not found".format(self.name))

    def delete(self):
        """Delete specified recipe from text file """
        while True:
            user_input = input("Confirm [Y|N]")

            if user_input.lower() == "y":
                # Delete entry
                # TODO
                pass
            else:
                print("Aborted deletion.")
                break
        pass

    def update(self):
        print("Updating textfile ...")
        with open(self.recipe_file, "w") as f:
            json.dump(self.recipes, f, indent=2)
        print("Updated file stored as \"{}\" in project folder.".format(self.recipe_file))

    def __str__(self):
        return "Current Recipe is \"{name}\" ".format(name=self.name)


if __name__ == '__main__':
    # Pfannkuchen = Recipe("Pfannkuchen", 4)
    # Output should be the needed ingredients for specified portion count

    Testkuchen = Recipe("Testkuchen", 4)

    Marmorkuchen = Recipe("Marmorkuchen", 1)

    Marmorkuchen.add_recipe({"category": "Kuchen",
                             "ingredient": [("Mehl", 500, "g"), ("Eier", 4)],
                             "instructions": "Immer fleißig rühren, dann wirds was und bei 200°C in den Ofen  Yippi Ya Yay :D"})

    Marmorkuchen.print_recipe()
    Marmorkuchen.print_recipe_list()
    Marmorkuchen.delete()
    Marmorkuchen.update()
