# DST
DST (Data Sweep Tool) is a tool used with UPPAAL that is able to test the sensitivity of models with respect to its parameters. An example of this might be that the cost of a product might be highly dependent on the time it is in development. However, it is not certain what the mean time of development is. Using DST, we can try different values for this parameter and see its influence on the yielded results of the model.

# How to install
* Clone the contents of [this repository][1] to your system using:

[1]: https://github.com/JaspervanRooijen/DST
~~~~ 
git clone https://github.com/JaspervanRooijen/DST
 ~~~~
* Create a virtual environment for the repository:
 ~~~~
python3 -m venv /path/to/new/virtual/environment
source /path/to/new/virtual/environment/bin/activate
~~~~
* Install the necessary python libraries using pip3. Necessary libraries are:
	* Flask (+ Jinja + Werkzeug) ([PyPI][2])
	````
	pip3 install flask
	````
	* BeautifulSoup4 ([PyPI][3])
	````
	pip3 install bs4
    ````
[2]:https://pypi.org/project/Flask/
[3]:https://pypi.org/project/beautifulsoup4/

After this DST should be functional by running:
````
python3 Controller.py
````

# Example
In the repository is a `/example/` directory with a file called `test.xml`. This file can be used to test whether DST is working and gives an example of how DST could be used.
First, let us start DST by running:
````
python3 Controller.py
````
We can access the tool at `127.0.0.1:5000`. There, we can upload a UPPAAL model, in this case the `test.xml`. After this, a new sweep can be added. At this point, a sweep over only one parameter is supported.

In this window a `start value ` and `ending value ` can be given, as well as a `step size` with which the value discreetly increases. The sweep can than be submitted.

After submitting the sweep a UPPAAL query can be given through the `Required data`field. This query can then be executed for every model in the parameter sweep.

For the `text.xml`example,  a `start value` of 15,  an `ending value` of 25 and a `stepping size` of 1 should work. An example of a valid query would be 
````
simulate [<= 30; 1] { Process.Finish }
````

After hitting `simulate` this should produce 10 graphs of at which point in time the Process is in the finished state.

