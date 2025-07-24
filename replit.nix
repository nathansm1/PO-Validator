
{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.tesseract
    pkgs.imagemagick
    pkgs.libGL
    pkgs.poppler_utils
  ];
}
