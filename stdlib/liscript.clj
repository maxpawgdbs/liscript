(def list (lambda () rest-args))

(def range
  (lambda (a b)
          (do
            (def recurse
              (lambda (nums x y)
                      (cond
                        (<= x y)
                        (recurse (cons y nums) x (- y 1))
                        nums)))

            (recurse () a b))))

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
            (def rec (lambda (arr2 rev)
                             (cond
                               (= arr2 ())
                               rev
                               (rec (cdr arr2) (cons (car arr2) rev)))))

            (rec arr1 ()))))

(symbol "LiScript dev version by october 2026")