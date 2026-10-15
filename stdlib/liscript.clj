(def list (lambda () rest-args))

(def range
  (lambda (a b)
          (do
            (def iter
              (lambda (nums x y)
                      (cond
                        (<= x y)
                        (iter (cons y nums) x (- y 1))
                        nums)))
            (iter () a b))))

(def is-prime
  (lambda
   (k)
   (cond
     (= 0 (% k 2)) (= k 2)
     (cond
       (< k 2)
       false
       (do
         (def check
           (lambda
            (i n)
            (cond
              (> (* i i) n)
              true
              (cond
                (= 0 (% n i))
                false
                (check (+ i 2) n)))))
         (check 3 k))))))

(def length
  (lambda
   (array)
   (do
     (def
       i 0
       iter (lambda
             (i array)
             (cond
               (= array ())
               i
               (iter (+ i 1) (cdr array)))))
     (iter i array))))

(def fib
  (lambda (n)
          (cond
            (< n 2)
            n
            (do
              (def iter
                (lambda (a b k)
                        (cond (= k 1)
                              b
                              (iter b (+ a b) (- k 1)))))
              (iter 0 1 n)))))

(def reverse
  (lambda (arr1)
          (do
            (def iter (lambda (arr2 rev)
                              (cond
                                (= arr2 ())
                                rev
                                (iter (cdr arr2) (cons (car arr2) rev)))))
            (iter arr1 ()))))

(def map
  (lambda (func array)
          (do
            (def iter
              (lambda (arrin arrout)
                      (cond
                        (= arrin ())
                        (reverse arrout)
                        (iter (cdr arrin) (cons (func (car arrin)) arrout)))))
            (iter array ()))))

(def filter
  (lambda (func array)
          (do
            (def iter
              (lambda (arrin arrout)
                      (cond
                        (= arrin ())
                        (reverse arrout)
                        (iter (cdr arrin) (cond (func (car arrin)) (cons (car arrin) arrout) arrout)))))
            (iter array ()))))

(def gcd (lambda (a b) (cond (= b 0) a (gcd b (% a b)))))

(def prime-factors
  (lambda
   (k) (do
         (def iter (lambda (i n array)
                           (cond (> (* i i) n)
                                 (reverse (cond (= n 1) array (cons n array)))
                                 (cond (= 0 (% n i))
                                       (iter i (/ n i) (cons i array))
                                       (iter (+ i 1) n array)))))
         (iter 2 k ()))))

(symbol "LiScript dev version by october 2026")