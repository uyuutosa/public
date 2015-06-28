#include<iostream>
#include<vector>
#include<opencv2/opencv.hpp>

using namespace std;


class cntname{
public:
	cntname(){ init("default"); }
	cntname(char* line){
		init(line);
	}

	void init(char* line){
		name = line;
		cnt = 0;
	}

	string operator()(){
		return name + to_string(++cnt);
	}


private:
	int cnt;
	string name;
}; 

class handle_cv
{
public:
	// constructors.
	handle_cv(char* filename){
		read_file(filename);
	}

	handle_cv(cv::Mat iimg){
		img = iimg;
	}

	handle_cv(const handle_cv &obj){
		img = obj.img;
	}

	// initialize.
	void init(){
		dname.init("default");
	}



	handle_cv(string);

	// File io.
	void read_file(char* filename);
	void show(char* name = "test", int wt = 0);
	void show_camera(char* name = "test");
		
	
	// Image processing.
	handle_cv bilateralFilter(int d, double sigmaColor, double sigmaSpace, int borderType = cv::BORDER_DEFAULT);
	handle_cv handle_cv::perspective_matrix(int lux1 = 0, int luy1=50, int ldx1=0, int ldy1=255,
		int rux1=255, int ruy1=50, int rdx1=255, int rdy1=255,
		int lux2=0, int luy2=0, int ldx2=100, int ldy2=255, int rux2=255, int ruy2=0, int rdx2=200, int rdy2=255);
	// object detection
	handle_cv detect_with_cascade(char* cascade_name);

	// Operators.
	//handle_cv operator = (handle_cv obj);

	

	cv::Mat img;
	cntname dname;// Default name.

private:
	
};


void handle_cv::read_file(char* filename){
	cv::Mat tmp = cv::imread(filename, 1);
	img.push_back(tmp);
}

void handle_cv::show(char* name, int wt){
	
	cv::imshow(strcmp(name, "test") ? name : dname(), img);
	cv::waitKey(wt);
}

void handle_cv::show_camera(char* name){
	cv::VideoCapture cap(0); // open the default camera
	string wname(strcmp(name, "test") ? name : dname());

	try{
		if (!cap.isOpened()) throw "cannot catch camera!";
	}
	catch (char* message){
		cout << message << endl;
		exit(1);
	}
	while (true){
		cv::Mat frame;
		cap >> frame;
		cv::imshow(wname, frame);
		if (cv::waitKey(30) >= 0) break;
	}

}

handle_cv handle_cv::bilateralFilter(int d, double sigmaColor, double sigmaSpace, int borderType){
	cv::Mat dst;
	cv::bilateralFilter(img, dst, d, sigmaColor, sigmaSpace, borderType);
	handle_cv ret(dst);
	return ret;
}

handle_cv handle_cv::perspective_matrix(int lux1, int luy1, int ldx1, int ldy1, int rux1, int ruy1, int rdx1, int rdy1,
	int lux2, int luy2, int ldx2, int ldy2, int rux2, int ruy2, int rdx2, int rdy2){
	cv::Point2f pts1[] = { cv::Point2f(lux1, luy1), cv::Point2f(ldx1, ldy1), cv::Point2f(rux1, ruy1),
		cv::Point2f(rdx1, rdy1) };
	cv::Point2f pts2[] = { cv::Point2f(lux2, luy2), cv::Point2f(ldx2, ldy2), cv::Point2f(rux2, ruy2),
		cv::Point2f(rdx2, rdy2) };
	cv::Mat perspective_matrix = cv::getPerspectiveTransform(pts1, pts2);
	cv::Mat dst = cv::getPerspectiveTransform(pts1, pts2);
	cv::warpPerspective(img, dst, perspective_matrix, img.size(), cv::INTER_LINEAR);
	handle_cv ret(dst);
	return ret;
}

handle_cv handle_cv::detect_with_cascade(char* cascade_name)
{
	// loading a cascade	
	//char *cascadeName = "cascade_cat.xml";
	//char *cascadeName = "haarcascade_frontalface_alt2.xml";
	cv::Mat dst = img.clone();
	cv::CascadeClassifier cascade;
	cascade.load(cascade_name);

	// detecting objects
	vector<cv::Rect> komas;
	cascade.detectMultiScale(dst, komas);

	// drawing rectangle of detecting area
	for (vector<cv::Rect>::iterator it = komas.begin(); it != komas.end(); ++it)
	{
		cv::rectangle(dst, cv::Rect(
			it->x, it->y, it->width, it->height), cv::Scalar(0, 255, 0), 4);
	}

	handle_cv ret(dst);
	return ret;
}

	// catch_camera
//handle_cv handle_cv::operator = (handle_cv obj){
//	init(obj);
//	return bil;
//}
