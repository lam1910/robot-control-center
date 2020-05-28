# ITSS Project Management for Embedded System

## Server for robot

## Hanoi University of Science and Technology and Uppsala Universitet

###### Group 5

1.	Team members:
	- Shehram Tahir
	- Lam Nguyen Ngoc
	- Tuong Phan Dinh
	- Nafi Uz Zaman
	- Anil Poudel
	- Bui Viet Dung
	- Quy Nguyen Ngoc
	- For more information. see [List of members](https://docs.google.com/presentation/d/1H9vXawhmfnKC6SyAqsgzui6CJ9gdFEHFe8S2NHvihdA/edit#slide=id.g842e3511ef_1_0)

2.	Techonology stack:
	- Python, server created using Django
	- Deploy to heroku

3.	APIs:
	- **GET** /path?start=(a, b)
	    - with: start is the start position of the robot either point A or point B

4.	Return:
	- For success, return HTTP 200 and a Json with 3 fields:
		- Mode: either Auto\(autonomous mode\), Manual\(manual mode\) and None\(do not have any instruction\)
		- Path: list of nodes the robot must cross; for manual mode, an empty list would be parsed
		- Move: list of directions (straight, left, right, reverse); for manual mode, a 1-element list would be parsed

	- For fail, ~~to be added~~
		- return HTTP 500 for internal error.
		- return HTTP 404 for when the server is unavailable

