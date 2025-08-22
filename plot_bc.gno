delay: 0.1
set yrange [0:]
set format x date
set xrange [2025-07-01:2025-08-25]
set xlabel "Date"
set ylabel "Known Cases"
f(x) = A*exp((x-datetime(2025, 7, 7)).days/B)
A = 103.13
B = 55.95
plot "bc_data/bc_measles.dat" using 1:2:3 with errorbars title "BC Measles Cases", f(x) title "Exponential Fit, Doubling Time = 38.8 days"
