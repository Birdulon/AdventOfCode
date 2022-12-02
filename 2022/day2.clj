(require '[clojure.string :as str])
(def filename "day2-input")
(def move-pairs (map #(str/split % #" ") (str/split-lines (slurp filename))))
(def move-map {"A" 1 "B" 2 "C" 3 "X" 1 "Y" 2 "Z" 3})
(defn draw-win-lose-score [our-move their-move]
    (get [3 6 0] (mod (- our-move their-move) 3)))
(defn part-1-round-score
    [move-pair]
    (let [
        [opposing-move our-move] move-pair
        op (get move-map opposing-move)
        us (get move-map our-move)
        ]
        (+ (draw-win-lose-score us op) us)))
(println (reduce + (map part-1-round-score move-pairs)))  ; Part 1
(defn part-2-round-score
    [move-pair]
    (let [
        [opposing-move our-move] move-pair
        op (get move-map opposing-move)
        us-move-offset (- (get move-map our-move) 2)
        us (+ (mod (+ (- op 1) us-move-offset) 3) 1)
        ]
        (+ (draw-win-lose-score us op) us)))
(println (reduce + (map part-2-round-score move-pairs)))  ; Part 2
