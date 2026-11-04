(def nil '())

(def nil? (lambda (l) (= l nil)))

(def list (lambda () rest-args))

(def defracro (racro (name args body) (def name (racro args body))))

(defmacro defn (name args)
  (list def
        name
        (list lambda
              args
              (cond
                (nil? rest-args) nil
                (nil? (cdr rest-args)) (car rest-args)
                (cons do rest-args)))))

(defn list? (l) (= "list" (typeof l)))

(defn symbol? (l) (= "symbol" (typeof l)))

(defracro += (x n) (set! x (+ x n)))

(defracro or-impl (z)
  (cond
    (nil? z) false
    (list cond (car z) true (or-impl (cdr z)))))

(defracro not (b) (= b false))

(defracro or () (or-impl rest-args))

(defn and-codegen (l)
  (cond
    (nil? l) true
    (list cond (car l) (and-codegen (cdr l)) false)))

(defracro and () (eval (and-codegen 'rest-args)))

(defn range (a b)
  (cond
    (<= a b) (cons a (range (+ a 1) b))
    nil))

(defn append (a b)
  (cond
    (nil? a) b
    (cons (car a) (append (cdr a) b))))

(defn merge-sort (array)
  (cond
    (<= (length array) 1) array
    (do (def
          split (lambda (arr k out)
                  (cond
                    (= k 0) out
                    (split (cdr arr) (- k 1) (cons (car arr) out)))))
        (def
          n (length array)
          left (merge-sort (split array (/ n 2) ()))
          right (merge-sort (split (reverse array) (+ (/ n 2) (% n 2)) ())))
        (def
          iter (lambda (a b ans)
                 (cond
                   (= a ()) (cond
                              (= b ()) ans
                              (iter a (cdr b) (cons (car b) ans)))
                   (cond
                     (= b ()) (iter (cdr a) b (cons (car a) ans))
                     (cond
                       (< (car a) (car b)) (iter (cdr a) b (cons (car a) ans))
                       (iter a (cdr b) (cons (car b) ans)))))))
        (reverse (iter left right ())))))

(def sort merge-sort)

(defn map (f l)
  (cond
    (nil? l) nil
    (cons (f (car l)) (map f (cdr l)))))

(defn filter (f a)
  (cond
    (nil? a) nil
    (f (car a)) (cons (car a) (filter f (cdr a)))
    (filter f (cdr a))))

(defn reduce (f a l)
  (cond
    (nil? l) a
    (reduce f (f a (car l)) (cdr l))))

(def foldl reduce)

(defn foldr (f a l)
  (cond
    (nil? l) a
    (f (foldr f a (cdr l)) (car l))))

(defn length (l) (foldl (lambda (a b) (+ a 1)) 0 l))

(defn reverse (l) (foldl (lambda (a e) (cons e a)) nil l))

(defn drop (n l)
  (cond
    (<= n 0) l
    (nil? l) nil
    (drop (- n 1) (cdr l))))

(defn take (n l)
  (cond
    (<= n 0) nil
    (nil? l) nil
    (cons (car l) (take (- n 1) (cdr l)))))

(defn intersperse (e l)
  (cond
    (nil? l) ()
    (nil? (cdr l)) l
    (cons (car l) (cons e (intersperse e (cdr l))))))

(defn contains? (e l)
  (cond
    (nil? l) false
    (= e (car l)) true
    (contains? e (cdr l))))

(defn deep-map (f l)
  (cond
    (nil? l) nil
    (list? l) (cons (cond
                      (list? (car l)) (deep-map f (car l))
                      (f (car l)))
                    (deep-map f (cdr l)))
    (f l)))

(defn iter (f l) (map f l) ())

(defn init (n f) (map f (range 0 (- n 1))))

(defn all (f l)
  (cond
    (nil? l) true
    (f (car l)) (all f (cdr l))
    false))

(defn any (f l)
  (cond
    (nil? l) false
    (f (car l)) true
    (any f (cdr l))))

(defn is-prime (k)
  (cond
    (= 0 (% k 2)) (= k 2)
    (< k 2) false
    (do (defn check (i n)
          (cond
            (> (* i i) n) true
            (= 0 (% n i)) false
            (check (+ i 2) n)))
        (check 3 k))))

(defn fib (n)
  (cond
    (< n 2) n
    (do (def
          iter (lambda (a b k)
                 (cond
                   (= k 1) b
                   (iter b (+ a b) (- k 1)))))
        (iter 0 1 n))))

(defn gcd (a b)
  (cond
    (= b 0) a
    (gcd b (% a b))))

(defn prime-factors (k)
  (do (def
        iter (lambda (i n array)
               (cond
                 (> (* i i) n) (reverse (cond
                                          (= n 1) array
                                          (cons n array)))
                 (cond
                   (= 0 (% n i)) (iter i (/ n i) (cons i array))
                   (iter (+ i 1) n array)))))
      (iter 2 k ())))

(defn fast-pow (x y)
  (do (def
        iter (lambda (a b res)
               (cond
                 (= b 0) res
                 (cond
                   (= (% b 2) 1) (iter (* a a) (/ b 2) (* res a))
                   (iter (* a a) (/ b 2) res)))))
      (iter x y 1)))

(defn n-times (n f x)
  (cond
    (<= n 0) x
    (n-times (- n 1) f (f x))))

(defn inc (x) (+ x 1))

(defn repeat (n x)
  (cond
    (<= n 0) ()
    (cons x (repeat (- n 1) x))))

(defn error (s) (print s) (/ 1 0))

(defn list-ref (i l)
  (cond
    (< i 0) (error "Индекс меньше нуля")
    (nil? l) (error "Индекс больше размера")
    (= i 0) (car l)
    (list-ref (- i 1) (cdr l))))

(symbol "LiScript dev version by october 2026")