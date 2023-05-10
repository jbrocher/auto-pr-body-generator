import os
from typing import Union
from typing_extensions import Annotated
import openai

from prompt_generator import PromptGenerator
import typer
from pr_body_generator import PrBodyGenerator
from pr_parser import PrParser


def main(
    diff_file: str,
    output_file: Annotated[str, typer.Option()],
    pr_file: Annotated[Union[str, None], typer.Option()] = None,
):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    print("Parsing diff an generating prompts")
    prompt_generator = PromptGenerator(diff_file)
    prompts = prompt_generator.generate_prompts()

    print(f"generated {len(prompts)}, staring body generation...")

    pr_body_generator = PrBodyGenerator(openai, prompts)
    pr_body_generator.generate_body()

    prefix = ""
    if pr_file:
        parser = PrParser(pr_file)
        prefix = parser.prefix

    if output_file:
        with open(output_file, "w") as f:
            f.write(f"{prefix}\n")
            f.write(f"{PrParser.DELIMITER}\n")
            f.write(pr_body_generator.body)
    else:
        print(pr_body_generator.body)


if __name__ == "__main__":
    typer.run(main)
