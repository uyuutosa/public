{
   TCanvas *c  = new TCanvas("c","Contours",0,0,800,700);
   TF2 *f2 = new TF2("f2","0.1+1000*((1-(x-2)*(x-2))*(1-(y-2)*(y-2)))",1,3,1,3);
   f2->SetFillStyle(1000);
   f2->SetLineWidth(1);
   double contours[3];
   contours[0] = 500;
   contours[1] = 700;
   contours[2] = 900;
   f2->SetContour(3,contours);
   Int_t colors[3] = {kRed, kYellow, kGreen};
   gStyle->SetPalette(3,colors);
   f2->Draw("cont0");  // Draw the fill area contour
   f2->Draw("cont3 same"); // draw the line contour on top
}
