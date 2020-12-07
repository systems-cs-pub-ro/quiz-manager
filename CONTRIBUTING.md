## Contributing to Quiz Manager
👍🎉 First off, thanks for taking the time to contribute! 🎉👍

The following is a set of guidelines for contributing to [Quiz Manager](https://github.com/systems-cs-pub-ro/quiz-manager). These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

### Code of Conduct
This project and everyone participating in it is governed by the [Code of Conduct](../blob/master/CODE_OF_CONDUCT.md). By participating, we kindly ask you to uphold this code. 

### Getting started
1. Create your own fork of the code
2. Do the changes in your fork
3. Send a pull request indicating what you added / modified. 

### Pull Requests
The process described here has several goals:
* Maintain Quiz Manager's quality
* Fix problems that are important in order to generate quizzes
* Engage the community in working toward the best possible Quiz Manager
* Enable a sustainable system for maintainers to review contributions
 
Please add in your Pull Request (PR) the following information to be considered by the maintainers:
1. For Bug Fixing
  * Identify the Bug: Link to the issue describing the bug that you're fixing. If there is not yet an issue for your bug, please open a new issue and then link to that issue in your pull request.
  * Description of the Change
  * Alternative Designs / Possible Drawbacks
2. For Adding, Changing, or Removing a Feature
  * Description of the Change
  * Verification Process. Try answering the following question: How did you verify that all new / changed functionality works as expected?

Working on your first Pull Request? You can learn how from this free series, [How to Contribute to an Open Source Project on GitHub](https://egghead.io/series/how-to-contribute-to-an-open-source-project-on-github) or follow the steps in [Git Immersion Tutorial](https://gitimmersion.com/).

### How to suggest a feature or enhancement

If you find yourself wishing for a feature that doesn't exist in the Quiz Manager, you are probably not alone. Open an issue on our issues list on GitHub which describes the feature you would like to see, why you need it, and how it should work.

## Styleguides
### Git Commit Messages
* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Prefix the commit messages with the component in Quiz Manager
  * `collection`: For improving the collector / collection component
  * `generator`: For improving the generator component
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

### Python Style Guide
We follow the [PEP8 style guide for Python](http://www.python.org/dev/peps/pep-0008/). Please use `pycodestyle` and `pylint` on your Python code. Use your best judgement to interpret their reports.
#### Template for functions 
Please consider documenting your code and the following template for functions and documentation of the functions:

    def fooFunction(a, b, c):
      """
      Gives the name of the best bar in town

      :param a: this is the first parameter
      :param b: this is the second parameter
      :param c: this is the third parameter
      :return: a string representing the name
      """

      return 'FooBar'

### Attribution
This CONTRIBUTING.md is adapted from [Atom](https://github.com/atom/atom/blob/master/CONTRIBUTING.md), [ember.js](https://github.com/emberjs/ember.js/blob/master/CONTRIBUTING.md), [Node.js](https://github.com/nodejs/node/blob/master/CONTRIBUTING.md), [Nayafia's Template](https://github.com/nayafia/contributing-template/blob/HEAD/CONTRIBUTING-template.md).