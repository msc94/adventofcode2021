use std::cmp;
use std::fmt;
use std::fs::File;
use std::io::{BufRead, BufReader};

use scan_fmt::scan_fmt;

const SIZE: usize = 1000;

#[derive(Debug, Clone, Copy)]
struct Point {
    x: i32,
    y: i32,
}

#[derive(Debug)]
struct Line {
    start: Point,
    end: Point,
}

#[derive(Debug)]
struct Playfield {
    points: Vec<Vec<i32>>,
}

impl Playfield {
    fn add_line(&mut self, line: &Line) {
        let start = line.start;
        let end = line.end;

        if start.x == end.x {
            let x = start.x;
            let min = cmp::min(start.y, end.y);
            let max = cmp::max(start.y, end.y);

            for y in min..=max {
                self.points[y as usize][x as usize] += 1;
            }
        } else if start.y == end.y {
            let y = start.y;
            let min = cmp::min(start.x, end.x);
            let max = cmp::max(start.x, end.x);

            for x in min..=max {
                self.points[y as usize][x as usize] += 1;
            }
        } else {
            // println!("Line is neither horizontal nor vertical: {:?}", line);

            let (sx, sy, ex, ey) = (start.x, start.y, end.x, end.y);
            let (dx, dy) = ((ex - sx).signum(), (ey - sy).signum());

            let (mut x, mut y) = (sx, sy);
            while x != ex || y != ey {
                self.points[y as usize][x as usize] += 1;
                x += dx;
                y += dy;
            }
        }
    }

    fn get_dangerous_points(&self) -> i32 {
        let mut num = 0;

        let points = self.points.iter().flatten();
        for p in points {
            if *p >= 2 {
                num += 1;
            }
        }

        num
    }
}

impl Default for Playfield {
    fn default() -> Self {
        Playfield {
            points: vec![vec![0; SIZE]; SIZE]
        }
    }
}

impl fmt::Display for Playfield {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for row in &self.points {
            write!(f, "{:?}\n", row).unwrap();
        }

        Ok(())
    }
}

fn read_lines(filename: &str) -> Vec<String> {
    let file = File::open(filename).expect("Opening file failed");

    BufReader::new(file).lines().map(|l| l.unwrap()).collect()
}

fn parse_line(line: &str) -> Line {
    let (start_x, start_y, end_x, end_y) =
        scan_fmt!(line, "{d},{d} -> {d},{d}", i32, i32, i32, i32).expect("Parsing failed");

    Line {
        start: Point {
            x: start_x,
            y: start_y,
        },
        end: Point { x: end_x, y: end_y },
    }
}

fn main() {
    let filename = "task5/input.txt";
    let lines = read_lines(filename);

    let line_vector: Vec<Line> = lines.iter().map(|l| parse_line(l)).collect();

    // println!("Lines: {:?}", line_vector);
    let mut field = Playfield::default();
    for line in line_vector {
        field.add_line(&line);
    }

    println!("Field now looks like:\n{}", field);
    println!("Result: {}", field.get_dangerous_points());
}
