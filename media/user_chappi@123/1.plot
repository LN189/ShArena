reset
set term png
set output "1.png"
set xrange [-5:5]
set xtics -4,2,4
set yrange [-5:5]
set ytics -4,2,4
set zrange [0:1000]
set ztics 0,200,1000
set ticslevel 0
set pm3d 
f(x,y) =(x+y>0)? (x+y)**3 : -1
splot f(x,y) lt 2 title "func(x,y)"
set output
