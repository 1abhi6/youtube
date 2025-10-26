from fastmcp import FastMCP
import os


# Create a FastMCP app
mcp = FastMCP(name="Video 2")


# 1. Define a Resource: Information about your company
@mcp.resource(
    "resource://company_info",
    name="Company Info",
    description="Provides information about InnoWave Technologies, a leading provider of AI-powered solutions.",
)
def company_info() -> str:
    """
    Return the information about the InnoWave Technologies.
    """
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "resource.txt")

    try:
        with open(file_path, "r", encoding="utf-8") as file_obj:
            return file_obj.read()
    except FileNotFoundError:
        return f"Error: resource.txt not found at {file_path}"
    except Exception as e:
        return f"An error occurred: {e}"


# 2. Define a Prompt: A reusable prompt for creating a job description
@mcp.prompt(
    name="Create Job Description",
    description="Creates a job description for a given role, using the company information.",
)
def create_jd(job_title: str) -> str:
    """
    Return the prompt to generate the JD.
    Args:
    job_title: Job Title
    """
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "prompt.txt")

    try:
        with open(file_path, "r", encoding="utf-8") as file_obj:
            template = file_obj.read()

        # Inject {job_title} placeholders
        return template.format(job_title=job_title)

    except FileNotFoundError:
        return f"Error: prompt.txt not found at {file_path}"
    except Exception as e:
        return f"An error occurred: {e}"


# 3. Define a Tool: A tool to post the job description to a job search website
@mcp.tool(
    name="post-job-description", description="Posts a job description to LinkedIn"
)
def post_to_linkedin(job_description: str):
    """Posts a job description to LinkedIn."""

    """
    
    
    """
    print(f"Posting to LinkedIn: {job_description}")
    return "Job description posted to LinkedIn successfully!"


if __name__ == "__main__":
    mcp.run()
