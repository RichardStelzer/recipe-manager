"""
Recipe manager / portion calculator for custom recipes
"""

import json


class Recipe:
    name = ""
    portions = int()
    category = ""
    ingredients = []
    instructions = ""
    recipes = {}
    recipe_file = "recipes.txt"

    def __init__(self, name, target_portions):
        """
        Load recipe if it is part of the recipe collection or add new recipe
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
                for ingredient in recipe["ingredients"]:
                    if ingredient[1].isnumeric():
                        ingredient[1] = float(ingredient[1])
                self.ingredients = recipe["ingredients"]
                self.instructions = recipe["instructions"]
                self.print_recipe(target_portions)
                exists = True
                break

        if not exists:
            self.portions = target_portions
            self.add_new_recipe()

    def add_new_recipe(self):
        """ Add new recipe to recipe collection stored in textfile

        data = {
            name: "Pfannkuchen",
            base_portions: 4,
            category: "Suesspeisse",
            ingredients: [ ("Eier", 4), ("Mehl", 150, "g"), ("Milch", 100, "ml") ],
            instructions: "Ruehr alles zusammen und brate alles in der Pfanne ordentlich an :D"
            }
        """
        print("Recipe with name \"{}\" not found in recipe collection".format(self.name))
        print("Adding new recipe ...")

        name = self.name
        target_base_portions = self.portions

        # Add category, e.g. "Kuchen"
        while True:
            ui_category = input("Enter category and confirm with \"Enter\":")  # "ui" == user input
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
                    ui_quantities = input("Specify quantity. Separated by comma if unit is used e.g. \"400,g\" or \"4\"")

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
            if ui_instruction:
                self.instructions = ui_instruction
                add_instructions = False

        #   Update textfile
        self.recipes.append({
            "name": self.name,
            "category": self.category,
            "portions": self.portions,
            "ingredients": self.ingredients,
            "instructions": self.instructions
        })

        self.update()

    def print_recipe(self, target_portions):
        """ Print recipe for specified portions """

        print("------------")
        print("Recipe: {} for {} portions".format(self.name, target_portions))

        multiplier = target_portions / self.portions
        for ingredient in self.ingredients:
            calculated_quantity = ingredient[1] * multiplier

            if calculated_quantity.is_integer():
                calculated_quantity = str(int(calculated_quantity))
            else:
                calculated_quantity = str(round(calculated_quantity, 1))

            if len(ingredient) > 2:
                print("- {}: {} {}".format(ingredient[0], calculated_quantity, " ".join(ingredient[2:])))
            else:
                print("- {}: {}".format(ingredient[0], calculated_quantity))

        # Print instructions with ~50 chars per line, so it looks pretty
        instructions = ""
        add_new_line = False
        for count, char in enumerate(self.instructions):
            if (count / 50).is_integer() and count > 0:
                add_new_line = True
            if add_new_line and char == " ":
                instructions += "\n"
                add_new_line = False
                continue
            instructions += char

        print("\n{}".format(instructions))
        print("------------")

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

    def delete_recipe(self):
        """Delete current recipe from text file """
        while True:
            user_input = input("Type \"{}\" to delete this recipe.".format(self.name))

            if user_input == self.name:
                # Delete entry
                self.recipes = [i for i in self.recipes if not (i["name"] == self.name)]

                # Identical :D
                # for idx, recipe in enumerate(self.recipes):
                #     if recipe["name"] == self.name:
                #         del self.recipes[idx]
                #         break
                self.update()
                break
            else:
                print("Aborted deletion.")
                break

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

    Testkuchen = Recipe("Testkuchen", 8)

    Marmorkuchen = Recipe("Marmorkuchen", 1)

    Marmorkuchen.add_recipe({"category": "Kuchen",
                             "ingredient": [("Mehl", 500, "g"), ("Eier", 4)],
                             "instructions": "Immer fleißig rühren, dann wirds was und bei 200°C in den Ofen  Yippi Ya Yay :D"})

    Marmorkuchen.print_recipe()
    Marmorkuchen.print_recipe_list()
    Marmorkuchen.delete()
    Marmorkuchen.update()
