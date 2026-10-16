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

(def fast-pow
  (lambda (x y)
          (do
            (def iter (lambda  (a b res) (cond (= b 0) res
                                               (cond (= (% b 2) 1)
                                                     (iter (* a a) (/ b 2) (* res a))
                                                     (iter (* a a) (/ b 2) res)))))
            (iter x y 1))))

(def merge-sort (lambda (array)
                        (cond (<= (length array) 1)
                              array
                              (do
                                (def split (lambda (arr k out)
                                                   (cond (= k 0)
                                                         out
                                                         (split (cdr arr) (- k 1) (cons (car arr) out)))))
                                (def n (length array)
                                  left (merge-sort (split array (/ n 2) ()))
                                  right (merge-sort (split (reverse array) (+ (/ n 2) (% n 2)) ())))
                                (def iter (lambda (a b ans)
                                                  (cond
                                                    (= a ())
                                                    (cond (= b ()) ans (iter a (cdr b)  (cons  (car b) ans)))
                                                    (cond (= b ())
                                                          (iter (cdr a) b (cons (car a) ans))
                                                          (cond (< (car a) (car b)) (iter (cdr a) b (cons (car a) ans)) (iter a (cdr b)  (cons  (car b) ans)))))))
                                (reverse (iter left right ()))))))

(def sort merge-sort)

(symbol "LiScript dev version by october 2026")