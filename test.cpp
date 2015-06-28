#include "handle_cv.h"

using namespace std;

int
main(int argc, char *argv[])
{
	//handle_cv a("Parrots.bmp");
	handle_cv a("test.jpg");
	handle_cv b = a.bilateralFilter(11, 50, 100);
	handle_cv c = b.detect_with_cascade("haarcascade_frontalface_alt2.xml");
	handle_cv d = b.perspective_matrix();

	a.show();
	b.show();
	c.show();
	d.show();
}
