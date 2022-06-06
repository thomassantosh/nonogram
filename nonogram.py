import sys
import re
import random
import numpy as np
import pandas as pd
from PIL import Image
from pixelate import pixelate
import imgkit


class Nonogram:
    def __init__(self):
        self.filepath = self.random_image()
        self.img_name = self.filepath.split('/')[-1:][0].split('.png')[0]
        # Filepaths
        self.pixeled_image = './results/' + str(self.img_name) + '_pixelated.png'
        self.grayscale_pixelized_image = './pixelized_grayscale_image.png'
        self.puzzle_image = './results/' + str(self.img_name) + '_puzzle.png'
        self.final_solution = './results/' + str(self.img_name) + '_nonogram_solution.png'
        # CSS elements
        self.caption_style={'selector': 'caption','props': 'caption-side: top; font-size:1.25em;'}
        self.index_names = {'selector': '.index_name','props': 'font-style: italic; color: darkgrey; font-weight:normal;'}
        self.headers = {'selector': 'th:not(.index_name)','props': 'background-color: #000066; color: white;'}
        # Main workflows
        self.dataframe = self.img_to_df()
        self.dataframe_shape = f"Dataframe shape: {self.dataframe.shape}"
        self.row_clues = self.generate_hints(self.dataframe,self.dataframe.columns,'rows')
        self.column_clues = self.generate_hints(self.dataframe,self.dataframe.columns)
        self.create_puzzle = self.puzzle()
        self.row_mapping = self.indexmap()
        self.col_mapping = self.columnmap()
        self.final_nonogram_image = self.generate_nonogram()
        self.create_pdf_document = self.create_pdf()

    def random_image(self):
        random_image_path = random.choice([
            './imgs/coffee.png', './imgs/cupcake.png', './imgs/snowflake.png', './imgs/unicorn.png'
            ])
        return random_image_path

    # Open image to dataframe
    def img_to_df(self):
        """Convert image into dataframe"""
        with open(self.filepath, 'rb') as f:
            im = Image.open(f)
            pixelate(self.filepath, self.pixeled_image, 50)

        # Convert to grayscale, resize to 15x15 pixels, convert to array
        with open(self.pixeled_image, 'rb') as f:
            im = Image.open(f)
            grayscale = im.convert('L')
            #grayscale.save(self.grayscale_pixelized_image)
            grayscale_resized = grayscale.resize((15,15),resample=Image.BILINEAR)
            grayscale_numpy_array = np.asarray(grayscale_resized)
            converted_array = np.where(grayscale_numpy_array == 255,0,1)

        return pd.DataFrame(converted_array)

    def generate_hints(self, df=None, range_index=None, col_type='columns'):
        """Function to capture row and column nonogram clues"""
        clues=[]
        
        for i in range_index:
            # Get the string value of clues
            if col_type=='columns':
                arr = df.iloc[:,i].values
            elif col_type=='rows':
                arr = df.loc[i,:].values
            arr = arr.tolist()
            a = "".join(str(x) for x in arr)
    #         print(f"String value for row/column {i} is {a}")
        
            # Find the combinations
            check_if_match = re.search('1', a)
            if check_if_match:
                result = re.findall('(1+)', a)
                result_length = [str(len(x)) for x in result]
                string_of_digits = "<br>".join(result_length)
    #             print(f"String of digits for row/column {i} is {string_of_digits}")
                clues.append(string_of_digits)
            else:
                clues.append('0')
        return clues


    def binary_coloring(self, v,props=''):
        return 'color:darkgrey;background-color:darkgrey' if v == 0 else 'color:grey;background-color:grey'

    def indexmap(self):
        mapping = {}
        for i in self.dataframe.index:
            mapping[i] =self.row_clues[i]
        return mapping

    def columnmap(self):
        mapping = {}
        for i in self.dataframe.columns:
            mapping[i] =self.column_clues[i]
        return mapping

    def puzzle(self):
        """Generate empty puzzle out of image properties"""
        shell = pd.DataFrame(data="", index=self.row_clues, columns=self.column_clues)
        styled_shell = shell.style.set_table_styles([self.caption_style, self.index_names,self.headers]).\
                set_caption("Puzzle")
        imgkit.from_string(styled_shell.to_html(), self.puzzle_image)


    def generate_nonogram(self):
        """Generate final solution nonogram"""
        # Define functions to map row and column clues
        func_index = lambda s: self.row_mapping[s]
        func_columns = lambda s: self.col_mapping[s]

        final_styled_df = self.dataframe.style.applymap(self.binary_coloring).\
                set_table_styles([self.caption_style, self.index_names, self.headers]).\
                set_caption("Solution").\
                format_index(func_index, axis=0).\
                format_index(func_columns, axis=1)

        imgkit.from_string(final_styled_df.to_html(), self.final_solution)

    def create_pdf(self):
        """Create PDF of original, pixelated, puzzle and solution"""
        original = Image.open(self.filepath)
        original = original.convert('RGB')

        pixelated = Image.open(self.pixeled_image)
        pixelated = pixelated.convert('RGB')

        puzzle = Image.open(self.puzzle_image)
        puzzle = puzzle.convert('RGB')
        
        solution = Image.open(self.final_solution)
        solution = solution.convert('RGB')
 
        imagelist = [pixelated, puzzle, solution]

        original.save('./results/' + str(self.img_name) + '_PDFimages.pdf',save_all=True, append_images=imagelist)


def main():
    nonogram = Nonogram()
    if nonogram:
        print("Process completed.")
    else:
        print("Process not completed!")

if __name__ == "__main__":
    main()
