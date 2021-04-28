## FetchRewards SDET Assessment
#### FetchFakeBars for Rewards
**URL:** [Playground URL](http://ec2-54-208-152-154.compute-1.amazonaws.com/)

### Approach
* Clean **Regression Test Scenario** with random-behavioral input for every step played by the script.
* Given constrain all bars have equal weigths, when a scale is unbalanced, test the weights from the lighter scale.
* Add weights in each step to both scales, if `=` proceed adding, in case of imbalance test scales on either ends.
* If not found, cointinue adding
* In case we use up all weights, so that values are not duplicated on either end of scale, we reset our current play and restart
* Used `Pure Pythonic Selenium` Scripts and tested with **Firefox browser v88.0 (64-bit)** on **Ubuntu 18.04** with an existing **Geckodriver v0.29.0 (cf6956a5ec8e 2021-01-14 10:31 +0200)**

### Dependencies
* Python 3 - [Download Python3](https://www.python.org/downloads/)
* Pip3 Package Manager - Packages mentioned in `requirements.txt`, downloaded by default along with Python3+
* [Download FireFox Browser](https://www.mozilla.org/en-US/firefox/new/), [Download GeckoDriver](https://github.com/mozilla/geckodriver/releases) - Mozilla Firefox Browser latest, [GeckoDriver Installation Procedures](https://firefox-source-docs.mozilla.org/testing/geckodriver/Usage.html) to control FireFox browser through Selenium.
* The Selenium dependencies and other python dependencies are installed by pip, with dependencies in `requirements.txt`. Refer [Python venv docs](https://docs.python.org/3/tutorial/venv.html)

### Data Structures
* **bars** - **List** of all bars weighted from `0 to maxBars`
* **visitedBars** - Boolean **List** to keep track of selected weight bars
* **leftScale, rightScale** - **Dictionary** mapping from board Index to corresponding weight

### Module Definitions
* `def setUp` - Instatiate Class Members and data Structures plus the driver Object for Selenium WebDriver
* `def test_grid` - Test Case to simulate the regression of user behavior.
* `def reset_scales` - In case we have exhausted weights by selecting all weights, then reset counters `leftScales, rightScales`
* `def generate_grid_scales` - Given a small grid <0,9> - Add an unseen value to both grid randomly generated from list of unselected weights and add to the scales.
* `def weigh_scales` - click `weigh` button and call `get_score_listings()`
* `def get_score_listing` - get the `game-info` list elements, the last value will have the recent weighed simulated value, capture that with xpath and call `find_fake_bar`
* `def find_fake_bar()` - Iterate over all cells, if cell has some value, the click the respective `coin divisioned cell`, check the `AlertBox` grab the text using `close_alert_and_get_its_text` method test for `Yay! You find it!`. Else `continue`.
* `def close_alert_and_get_its_text` - Utility to switch from Browser to textBox and capture the text, return the text for assertion.

### Set-Up
*Prereq: Complete Dependencies section and proceed*
* Download the project zip.
* Unzip the project, which has the project_directory `project_dir/`
* `cd FetchRewards_27Apr21/`
* Run `python3 -m venv env` - to trigger virtual env instance for Python to keep existing deps on machine safe.
* **Linux/Mac machine**Run `source env/bin/activate` - Activate the virtual environment, Refer [Python venv Docs](https://docs.python.org/3/library/venv.html) for Windows Platform.
* Run `pip install -r requirements.txt` - Install dependencies `Selenium` and other required Packages
* Run `python testBars.py` - Runs Python Script to test the WebApp, by launching FireFox browser. **Completer Set-Up and previous steps before execution** 

### Challenges
* `self.driver.find_element_by_id("reset").click()`
Had trouble calling this method from member functions
* `Random Pattern to Test` - Took a while to implement and test - **Why?** - guarantees no duplicates, and tests every behavior of the board.
* *Better Approach* - Shuffle the weights to new scales on board with unweighed scale to find the fake bar in a shorter time

### References
* [Selenium Docs](https://selenium-python.readthedocs.io/locating-elements.html)