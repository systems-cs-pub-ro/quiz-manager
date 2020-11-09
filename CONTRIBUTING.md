## Contributing to Quiz Manager
👍🎉 First off, thanks for taking the time to contribute! 🎉👍

The following is a set of guidelines for contributing to Quiz Manager, which is hosted in the [Systems Organization](https://github.com/systems-cs-pub-ro) on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

### Code of Conduct
This project and everyone participating in it is governed by the [Code of Conduct](../blob/master/CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. 

### Getting started
1. Create your own fork of the code
2. Do the changes in your fork
3. Send a pull request indicating that you added / modified. 

### Pull Requests
The process described here has several goals:
* Maintain Quiz Manager's quality
* Fix problems that are important in order to generate quizes
* Engage the community in working toward the best possible Quiz Manager
* Enable a sustainable system for maintainers to review contributions
 
Please add in you PR the following information to be considered by the maintainers:
1. For Bug Fixing
  * Identify the Bug: Link to the issue describing the bug that you're fixing. If there is not yet an issue for your bug, please open a new issue and then link to that issue in your pull request.
  * Description of the Change
  * Alternative Designs / Possible Drawbacks
2. For Adding, Changing, or Removing a Feature
  * Description of the Change
  * Verification Process. Try answering the following question:
    * How did you verify that all new functionality works as expected?
    * How did you verify that all changed functionality works as expected?

Working on your first Pull Request? You can learn how from this free series, [How to Contribute to an Open Source Project on GitHub](https://egghead.io/series/how-to-contribute-to-an-open-source-project-on-github) or follow the steps in [Git Immersion Tutorial](https://gitimmersion.com/).

### How to report a bug
Any security issues should be submitted directly to [MAIL]  in order to determine whether you are dealing with a security issue, ask yourself these two questions:
* Can I access something that's not mine, or something I shouldn't have access to?
* Can I disable something for other people?
If the answer to either of those two questions are "yes", then you're probably dealing with a security issue. Note that even if you answer "no" to both questions, you may still be dealing with a security issue.
 
When filing an issue, make sure to answer these five questions:
1.What version of Go are you using (go version)?
2. What operating system and processor architecture are you using?
3. What did you do?
4. What did you expect to see?
5. What did you see instead?

### How to suggest a feature or enhancement

If you find yourself wishing for a feature that doesn't exist in the Quiz Manager, you are probably not alone. Open an issue on our issues list on GitHub which describes the feature you would like to see, why you need it, and how it should work.

### Styleguides
### Git Commit Messages
* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line
* Consider starting the commit message with an applicable emoji:
* 🎨 :art: when improving the format/structure of the code
* 🐎 :racehorse: when improving performance
* 🚱 :non-potable_water: when plugging memory leaks
* 📝 :memo: when writing docs
* 🐧 :penguin: when fixing something on Linux
* 🍎 :apple: when fixing something on macOS
* 🏁 :checkered_flag: when fixing something on Windows
* 🐛 :bug: when fixing a bug
* 🔥 :fire: when removing code or files
* ✅ :white_check_mark: when adding tests
* 🔒 :lock: when dealing with security
* 👕 :shirt: when removing linter warnings

### Issue and Pull Request Labels
#### Issues Labels
| *Issues*  | *Description*|
| `bug`   | Confirmed bugs or reports that are very likely to be bugs.|
| `question`  | Questions more than bug reports or feature requests (e.g. how do I do X).|

#### Pull Request Labels
| *Label name*  | *Description*|
| `work-in-progress`   | Pull requests which are still being worked on, more changes will follow.|
| `needs-review`  | Pull requests which need code review, and approval from maintainers. |
| `under-review`  | Pull requests being reviewed by maintainers. |
| `requires-changes` | Pull requests which need to be updated based on review comments and then reviewed again.|

### Attribution
This CONTRIBUTING.md is adapted from [Atom](https://github.com/atom/atom/blob/master/CONTRIBUTING.md), [ember.js](https://github.com/emberjs/ember.js/blob/master/CONTRIBUTING.md), [Node.js](https://github.com/nodejs/node/blob/master/CONTRIBUTING.md), [Nayafia's Template](https://github.com/nayafia/contributing-template/blob/HEAD/CONTRIBUTING-template.md).