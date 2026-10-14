(def n (read "Введите число ") out 1 k n fact '(cond (> n 1) (do (set! out (* out n)) (set! n (- n 1)) (eval fact)) 0))
(eval fact)
(print "Факториал" k "равен" out)
(symbol "")