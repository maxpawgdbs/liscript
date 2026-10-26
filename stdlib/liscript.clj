; Элементарные функции списков
(def nil '())
(def nil? (lambda (l) (= l nil)))
(def list (lambda () rest-args))
(def list? (lambda (l) (= "list" (typeof l))))
; Вспомогательные функции
(def defracro (racro (name args body) (def name (racro args body))))
(defmacro defn (name args)
  (list def name
        (list lambda args
              (cond (nil? rest-args) nil
                    (nil? (cdr rest-args)) (car rest-args)
                    (cons do rest-args)))))
(defmacro += (x n) (list set! x (list + x n)))
(defn or-impl (z) (cond (nil? z) false  (list cond (car z) true (or-impl (cdr z)))))
; Логические функции
(defn not (b) (= b false))
(defmacro or () (or-impl rest-args))
; Базовые функции списков
(defn length (array) (cond (nil? array) 0 (+ 1 (length  (cdr array)))))
(defn reverse (arr1)
  (do
    (def iter (lambda (arr2 rev)
                      (cond
                        (= arr2 ())
                        rev
                        (iter (cdr arr2) (cons (car arr2) rev)))))
    (iter arr1 ())))
(defn range (a b) (cond (<= a b) (cons a (range (+ a 1) b)) nil))
(defn append (array1 array2) (do
                               (def iter (lambda (a b)
                                                 (cond (= a ())
                                                       b
                                                       (iter (cdr a) (cons (car a) b)))))
                               (iter (reverse array1) array2)))
; Продвинутые функции списков
(defn merge-sort (array)
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
          (reverse (iter left right ())))))
(def sort merge-sort)
(defn map (f l) (cond (nil? l) nil (cons (f (car l)) (map f (cdr l)))))
(defn filter (f a) (cond (nil? a) nil (f (car a)) (cons (car a) (filter f (cdr a))) (filter f (cdr a))))
; Функции для чисел
(defn is-prime (k) (cond
                     (= 0 (% k 2)) (= k 2)
                     (< k 2) false
                     (do (defn check (i n) (cond
                                             (> (* i i) n) true
                                             (= 0 (% n i)) false
                                             (check (+ i 2) n)))
                         (check 3 k))))
(defn fib (n)
  (cond
    (< n 2)
    n
    (do
      (def iter
        (lambda (a b k)
                (cond (= k 1)
                      b
                      (iter b (+ a b) (- k 1)))))
      (iter 0 1 n))))
(defn gcd (a b) (cond (= b 0) a (gcd b (% a b))))
(defn prime-factors (k) (do
                          (def iter (lambda (i n array)
                                            (cond (> (* i i) n)
                                                  (reverse (cond (= n 1) array (cons n array)))
                                                  (cond (= 0 (% n i))
                                                        (iter i (/ n i) (cons i array))
                                                        (iter (+ i 1) n array)))))
                          (iter 2 k ())))
(defn fast-pow (x y)
  (do
    (def iter (lambda  (a b res) (cond (= b 0) res
                                       (cond (= (% b 2) 1)
                                             (iter (* a a) (/ b 2) (* res a))
                                             (iter (* a a) (/ b 2) res)))))
    (iter x y 1)))
; Вывод
(symbol "LiScript dev version by october 2026")