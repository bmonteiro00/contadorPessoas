#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <vector>

using namespace cv;
using namespace std;

#define AREA_PESSOA_MIN 2000
#define RED Scalar(0,0,255)

#define COLOR_SHAPE Scalar(0, 255, 0)

//Mat src; Mat src_gray;
RNG rng(12345);

int main(int,  char* argv[])
{
    //cuda::GpuMat dst, src; -> quadros para a GPU

	VideoCapture videoCapture(argv[1]);

    if(!videoCapture.isOpened())
        return -1;

    Mat front;
    Ptr<BackgroundSubtractor> backgroundSubstractor = createBackgroundSubtractorMOG2();
    namedWindow("ScreenPeople",1);
    for(;;)
    {
        Mat quadro;
        Mat quadroDebug;
		vector<vector<Point> > contadorContornos;
		vector<Vec4i> hierarquia;

		videoCapture >> quadro;
        line( quadro, Point(0,quadro.rows/2), Point(quadro.cols,quadro.rows/2), RED);

        cvtColor(quadro, quadro, COLOR_BGR2GRAY);
        backgroundSubstractor->apply(quadro, quadroDebug);

		threshold(quadroDebug, quadroDebug, 128, 255, THRESH_BINARY);

	    morphologyEx(quadroDebug, quadroDebug, MORPH_OPEN, Mat(8, 8, CV_8UC1, Scalar(1)));
		morphologyEx(quadroDebug, quadroDebug, MORPH_CLOSE, Mat(8, 8, CV_8UC1, cv::Scalar(1)));

		findContours(quadroDebug, contadorContornos, hierarquia, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);

		for (unsigned int i = 0; i < contadorContornos.size(); ++i)
		{
			if (contourArea(contadorContornos[i]) > AREA_PESSOA_MIN) {
				drawContours(quadroDebug, contadorContornos, 0, COLOR_SHAPE, 2, 8);
			}
		}

	   //imshow("ScreenPeople",frameDebug);
	   imshow("ScreenPeople",quadroDebug);

       if(waitKey(30) >= 0) break;
    }

    return 0;
}
