# 📦 Repopack-py

> Python version of [npm repopack](https://github.com/yamadashy/repopack) by [yamadashy](https://github.com/yamadashy)

Repopack is a powerful tool that packs your entire repository into a single, AI-friendly file.  
Perfect for when you need to feed your codebase to Large Language Models (LLMs) or other AI tools like Claude, ChatGPT, and Gemini.


Here is webapp for same use case, runs entirely on browser, fully static :- [repo2txt.simplebasedomain.com](https://repo2txt.simplebasedomain.com/)  [Code](https://github.com/abinthomasonline/repo2txt)


## 📊 Usage

To use Repopack-py, follow these steps:

1. Install the package:
   ```
   pip install repopack
   ```

2. Run the following command:
   ```
   repopack path/to/your/repository
   ```

4. The packed file will be generated in the current directory with the name `repopackpy-output.txt` by default.

### Options

You can customize the packing process with these options:

- `-o, --output`: Specify the output file name (default: repopack_output.txt)
- `-i, --ignore`: Add patterns to ignore (in addition to .gitignore, comma-separated)
- `-c, --config`: Specify a configuration file
- `--output-show-line-numbers`: Show line numbers in the output file
- `--output-style`: Specify the output style plain or xml (default: plain)
