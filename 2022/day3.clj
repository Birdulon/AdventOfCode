(require '[clojure.string :as str])
(require '[clojure.set])
(require '[clojure.zip :as zip])

(def elves (str/split-lines (slurp "input/3")))
(defn priority [char]
    (let [
        c (int char)
        a (int \a)
        z (int \z)
        A (int \A)
    ]
    (if (<= a c z)
        (+ (- c a) 1)
        (+ (- c A) 27))))

; Part 1
(defn two-knapsacks [line] (
    let [
        half (/ (count line) 2)
        [knapsack-1 knapsack-2] (map set (split-at half line))
    ]
    (priority (first (clojure.set/intersection knapsack-1 knapsack-2)
))))
(println (reduce + (map two-knapsacks elves)))

; Part 2
(defn chunker [sequence num]
    (if (<= (count sequence) num)
    [sequence]
    (let [[head tail] (split-at num sequence)] (lazy-seq (cons head (chunker tail num))))))
(defn three-elves [lines]
    (priority (first (apply clojure.set/intersection (map set lines)))))
(println (reduce + (map three-elves (chunker elves 3))))